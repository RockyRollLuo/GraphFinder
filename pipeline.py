#!/usr/bin/env python3
"""Anonymized GraphFinder pipeline.

This module contains the core method only. All remote model credentials are
read from environment variables and never persisted.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from ontology import ONTOLOGY


def call_remote(model, messages, max_tokens=2000, retries=3):
    key_env, url, model_name = {
        "deepseek": ("DEEPSEEK_API_KEY", "https://api.deepseek.com/chat/completions", "deepseek-chat"),
        "zhipu": ("ZHIPU_API_KEY", "https://open.bigmodel.cn/api/paas/v4/chat/completions", os.environ.get("ZHIPU_MODEL", "glm-4-flash")),
    }[model]
    key = os.environ.get(key_env)
    if not key:
        raise RuntimeError(f"Set {key_env} before using {model}")
    payload = json.dumps({"model": model_name, "messages": messages, "temperature": 0, "max_tokens": max_tokens}).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            print(f"remote retry {attempt + 1}: {exc}", file=sys.stderr, flush=True)
            time.sleep(2 * (attempt + 1))
    return ""


def parse_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except (json.JSONDecodeError, ValueError):
        return None


def slot_fill(problem, entry, model):
    template = entry.get("slot_template", {})
    slots = "\n".join(
        f"{key}: {value.get('type', 'unknown')} -> {value.get('maps_to', 'graph_element')}"
        if isinstance(value, dict) else f"{key}: {value}"
        for key, value in template.items()
    )
    prompt = (
        "You are an expert in graph theory and analogical reasoning.\n"
        f"GRAPH PROBLEM TYPE: {entry['name']}\n"
        f"TOPOLOGICAL SKELETON: {entry.get('topological_skeleton', '')}\n"
        f"TEMPLATE SLOTS:\n{slots}\n\n"
        f"DOMAIN PROBLEM:\n{problem}\n\n"
        "Fill every slot using exact problem text where possible. Use N/A when absent. "
        "Output only valid JSON."
    )
    return parse_json(call_remote(model, [{"role": "user", "content": prompt}], max_tokens=1200))


def codegen(formalization, model):
    prompt = (
        "Write a complete, self-contained Python 3 program that solves the formalized "
        "graph problem below using the standard library, NumPy, and NetworkX. "
        "Define solve() returning (solution, objective) and print one final JSON object "
        'with keys "solution" and "objective".\n\n'
        "FORMALIZED PROBLEM:\n" + json.dumps(formalization, indent=2)
    )
    answer = call_remote(model, [{"role": "user", "content": prompt}], max_tokens=2000)
    match = re.search(r"```(?:python)?\n(.*?)```", answer, re.DOTALL)
    return match.group(1) if match else answer


def execute(code, timeout=20):
    path = Path(".tmp_graphfinder_solver.py")
    path.write_text(code, encoding="utf-8")
    try:
        proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=timeout)
    finally:
        path.unlink(missing_ok=True)
    if proc.returncode != 0:
        return False, (proc.stderr or "runtime error")[:300]
    lines = [line for line in proc.stdout.strip().splitlines() if line.strip()]
    if not lines:
        return False, "no output"
    payload = parse_json(lines[-1])
    return bool(payload and "objective" in payload), str(payload)[:500]


def identify(problem, model):
    ontology_text = "\n".join(
        f"{key} ({entry['name']}): {entry['canonical_description']}"
        for key, entry in ONTOLOGY.items()
    )
    prompt = (
        "You are an expert in graph theory and combinatorial optimization.\n"
        "Identify the most likely ontology problem key for the following description.\n\n"
        f"ONTOLOGY:\n{ontology_text}\n\nPROBLEM:\n{problem}\n\n"
        "Output only the key."
    )
    answer = call_remote(model, [{"role": "user", "content": prompt}], max_tokens=100).strip()
    return answer.split()[0].strip(".,;") if answer else ""


def run(problem, model="deepseek"):
    key = identify(problem, model)
    entry = ONTOLOGY.get(key)
    if entry is None:
        return {"abstained": True, "identified_key": key}
    form = slot_fill(problem, entry, model)
    if form is None:
        return {"abstained": True, "identified_key": key, "schema_valid": False}
    code = codegen({"problem_type": entry["name"], "formalization": form}, model)
    ok, info = execute(code)
    return {
        "abstained": False,
        "identified_key": key,
        "schema_valid": True,
        "execution_success": ok,
        "output": info,
    }


def main():
    parser = argparse.ArgumentParser(description="GraphFinder anonymous pipeline")
    parser.add_argument("--problem", required=True)
    parser.add_argument("--llm", choices=("deepseek", "zhipu"), default="deepseek")
    args = parser.parse_args()
    print(json.dumps(run(args.problem, args.llm), indent=2))


if __name__ == "__main__":
    main()
