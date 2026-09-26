# GraphFinder

Anonymous implementation of the GraphFinder pipeline.

GraphFinder transforms a natural-language optimization problem into an
ontology-grounded graph formalization and an executable solver result.

## Contents

- `ontology.py`: curated ontology of classical graph problems and typed slot templates.
- `ontology_add1.py`, `ontology_add2.py`, `ontology_add3.py`: extension modules defining additional ontology entries.
- `pipeline.py`: admission, identification, typed slot filling, code generation, and execution gate.
- `pee.py`: problem-essence embedding training and inference.
- `README.md`: this file.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Credentials

No credential is stored in this repository. Before running remote LLM stages,
export the required environment variable:

```bash
export DEEPSEEK_API_KEY="..."
export ZHIPU_API_KEY="..."
```

The released method supports the `deepseek` and `zhipu` remote backends.

## Usage

```bash
python pipeline.py \
  --problem "A shipping line must send 100 containers from port A to port B ..." \
  --llm deepseek
```

The full benchmark, evaluation scripts, trained checkpoints, and raw results are released separately with the paper and are intentionally excluded from this anonymized method-only repository.

Results are written as JSON and never include credentials.

## Method Summary

1. A graphizability filter rejects inputs without an ontology-compatible graph abstraction.
2. Retrieval selects a classical graph-problem template with a topological skeleton.
3. Typed slot filling binds domain entities and constraints to graph components.
4. A semantic anchor table records the bidirectional domain-to-graph mapping.
5. Generated solver code is accepted only after programmatic execution checks.
