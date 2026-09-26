#!/usr/bin/env python3
"""
PEE (Problem Essence Embedding) Trainer
========================================
Trains a contrastive embedding model that maps natural-language problem
descriptions into a space where topological similarity determines proximity.

Training strategy:
  - Base model: sentence-transformers/all-mpnet-base-v2
  - Positive pairs: same graph problem, different domain descriptions
  - Hard negatives: same problem family, different problem class
  - Easy negatives: different problem family
  - Loss: Supervised Contrastive (SupCon) + MultiSimilarity
  - Conditioning: topological skeleton is prepended as a structural prior

Reference:
  Khosla et al., "Supervised Contrastive Learning", NeurIPS 2020.
  Wang et al., "Text Embeddings by Weakly-Supervised Contrastive Pre-training", 2023.
"""

import os
import sys
import json
import random
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import numpy as np

from sentence_transformers import SentenceTransformer, models, losses, InputExample
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ontology import ONTOLOGY, get_problems_by_family, get_family_counts, generate_descriptions

# ── Configuration ────────────────────────────────────────────────────────
EXPERIMENTS_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(EXPERIMENTS_DIR, "models", "pee")
DATA_DIR = os.path.join(EXPERIMENTS_DIR, "data")
RESULTS_DIR = os.path.join(EXPERIMENTS_DIR, "results")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

CONFIG = {
    "base_model": "sentence-transformers/all-mpnet-base-v2",
    "embedding_dim": 768,
    "max_seq_length": 512,
    "batch_size": 32,
    "num_epochs": 20,
    "learning_rate": 2e-5,
    "warmup_steps": 100,
    "temperature": 0.07,
    "skeleton_conditioning": True,
    "num_augmentations_per_problem": 8,
    "num_hard_negatives_per_batch": 4,
    "device": "cuda" if torch.cuda.is_available() else "cpu",
    "seed": 42,
}

random.seed(CONFIG["seed"])
np.random.seed(CONFIG["seed"])
torch.manual_seed(CONFIG["seed"])


# ══════════════════════════════════════════════════════════════════════════
# TRAINING DATA GENERATION
# ══════════════════════════════════════════════════════════════════════════

class ProblemDescriptionGenerator:
    """Generates diverse NL descriptions for each ontology entry."""

    def __init__(self, num_augmentations=8, skeleton_conditioning=True):
        self.num_aug = num_augmentations
        self.skeleton_conditioning = skeleton_conditioning

        # Hand-crafted domain-agnostic templates for each problem family
        self.family_templates = {
            "path": [
                "A company needs to move resources from {src} to {dst} through a network of {n} waypoints. Each possible direct connection has a {attr}: {edge_info}. {obj}",
                "In a {domain} network, determine the optimal traversal from {src} to {dst}. Connections between nodes have {attr}: {edge_info}. {obj}",
                "You are given {n} locations and {m} possible roads between them. Each road takes {attr}: {edge_info}. Find the best route from {src} to {dst} to {obj}.",
                "Model a {domain} system as nodes and directed edges. Edge weights represent {attr}: {edge_info}. {obj} from {src} to {dst}.",
            ],
            "flow": [
                "A {domain} network has {n} nodes and {m} connections. Each connection can handle up to {cap} units. {obj} from source {src} to sink {dst}.",
                "Design a {domain} distribution system with {n} stations connected by {m} pipes/links. Each link has capacity {cap}. {obj} from {src} to {dst}.",
                "Given a directed network of {n} vertices with {m} edges, each edge e has capacity c(e). {obj}.",
            ],
            "matching": [
                "We have {n} items of type A and {m} items of type B. Each pair has a compatibility value. {obj}",
                "Match {n} {type_a} to {m} {type_b} given a compatibility matrix. {obj}",
                "In a bipartite setting with {n} left nodes and {m} right nodes, edges represent feasible assignments. {obj}",
            ],
            "covering": [
                "Select a subset of {n} {items} such that every {relation} is {covered_by} at least one selected item. {obj}",
                "Place {resources} at vertices of a graph with {n} nodes and {m} edges. Each placed {resource} covers incident edges. {obj}",
            ],
            "partitioning": [
                "Divide {n} items into k groups based on pairwise {attr}. {obj}",
                "Partition a set of {n} elements into disjoint subsets. Pairs of elements have {attr} values. {obj}",
            ],
        }

        self.domain_words = {
            "path": {"src": ["Warehouse A", "Node Alpha", "Origin", "Depot"], "dst": ["Store B", "Node Omega", "Destination", "Terminal"],
                     "attr": ["travel time", "distance", "cost", "latency", "congestion level"],
                     "domain": ["transportation", "logistics", "communication", "supply chain"]},
            "flow": {"src": ["Source", "Reservoir", "Factory", "Supply Depot"], "dst": ["Sink", "Treatment Plant", "Warehouse", "Demand Point"],
                     "domain": ["water distribution", "oil pipeline", "data center", "traffic"]},
            "matching": {"type_a": ["workers", "students", "tasks", "doctors"], "type_b": ["jobs", "projects", "machines", "shifts"]},
            "covering": {"items": ["cameras", "sensors", "monitors", "guards"], "resources": ["camera", "sensor", "monitor", "guard"],
                         "relation": ["corridor", "link", "connection", "path"], "covered_by": ["monitored by", "covered by", "observed by", "guarded by"]},
            "partitioning": {"attr": ["similarity", "distance", "conflict", "compatibility"]},
        }

    def generate_one(self, problem_id: str, ontology_entry: dict) -> str:
        """Generate one NL description for a given ontology entry."""
        onto = ontology_entry
        skeleton = onto.get("topological_skeleton", "")
        objective = onto.get("core_objective", "")
        family = onto.get("family", "path")

        templates = self.family_templates.get(family, self.family_templates["path"])
        tmpl = random.choice(templates)

        dw = self.domain_words.get(family, self.domain_words["path"])
        n = random.randint(5, 50)
        m = random.randint(n, min(n * 5, 200))

        fill = {
            "n": n, "m": m,
            "src": random.choice(dw.get("src", ["Source"])),
            "dst": random.choice(dw.get("dst", ["Destination"])),
            "attr": random.choice(dw.get("attr", ["cost"])),
            "domain": random.choice(dw.get("domain", ["logistics"])),
            "cap": f"{random.randint(10, 100)} units",
            "edge_info": f"e.g., {random.randint(1,50)}min-{random.randint(1,50)}min per segment",
            "obj": objective,
            "type_a": random.choice(dw.get("type_a", ["items"])),
            "type_b": random.choice(dw.get("type_b", ["targets"])),
            "items": random.choice(dw.get("items", ["items"])),
            "resources": random.choice(dw.get("resources", ["resources"])),
            "relation": random.choice(dw.get("relation", ["connection"])),
            "covered_by": random.choice(dw.get("covered_by", ["covered by"])),
        }

        try:
            desc = tmpl.format(**fill)
        except (KeyError, ValueError):
            desc = tmpl
            for k, v in fill.items():
                desc = desc.replace("{" + k + "}", str(v))

        if self.skeleton_conditioning:
            desc = f"[Topological Structure: {skeleton}] {desc}"

        return desc

    def generate_all(self) -> List[Dict]:
        """Generate all training data: multiple descriptions per problem."""
        data = []
        for prob_id, onto in ONTOLOGY.items():
            for _ in range(self.num_aug):
                desc = self.generate_one(prob_id, onto)
                data.append({
                    "problem_id": prob_id,
                    "family": onto["family"],
                    "complexity": onto["complexity"],
                    "name": onto["name"],
                    "description": desc,
                })
        random.shuffle(data)
        return data


# ══════════════════════════════════════════════════════════════════════════
# CONTRASTIVE DATASET
# ══════════════════════════════════════════════════════════════════════════

class ContrastiveProblemDataset(Dataset):
    """Produces (anchor, positive, negatives) triplets for contrastive learning."""

    def __init__(self, data: List[Dict], num_hard_negatives=4):
        self.data = data
        self.num_hard_neg = num_hard_negatives
        # Group by problem_id for positive pair sampling
        self.by_problem = {}
        for i, d in enumerate(data):
            pid = d["problem_id"]
            self.by_problem.setdefault(pid, []).append(i)

        # Group by family for hard negative sampling
        self.by_family = {}
        for i, d in enumerate(data):
            fam = d["family"]
            self.by_family.setdefault(fam, []).append(i)

        self.all_problem_ids = list(self.by_problem.keys())
        self.all_families = list(self.by_family.keys())

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        anchor = self.data[idx]
        pid = anchor["problem_id"]
        family = anchor["family"]

        # Positive: same problem, different description
        same_problem_indices = [i for i in self.by_problem[pid] if i != idx]
        if same_problem_indices:
            pos_idx = random.choice(same_problem_indices)
        else:
            pos_idx = idx  # fallback
        positive = self.data[pos_idx]

        # Hard negatives: same family, different problem
        same_family_indices = self.by_family.get(family, [])
        hard_neg_candidates = [i for i in same_family_indices
                               if self.data[i]["problem_id"] != pid]
        if len(hard_neg_candidates) >= self.num_hard_neg:
            hard_neg_indices = random.sample(hard_neg_candidates, self.num_hard_neg)
        else:
            hard_neg_indices = hard_neg_candidates

        # Easy negatives: different family
        other_families = [f for f in self.all_families if f != family]
        if other_families:
            other_fam = random.choice(other_families)
            easy_neg_idx = random.choice(self.by_family[other_fam])
        else:
            easy_neg_idx = random.choice([i for i in range(len(self.data)) if i != idx])

        hard_negs = [self.data[i]["description"] for i in hard_neg_indices]
        easy_neg = self.data[easy_neg_idx]["description"]

        return {
            "anchor": anchor["description"],
            "positive": positive["description"],
            "hard_negatives": hard_negs,
            "easy_negative": easy_neg,
            "problem_id": pid,
            "family": family,
        }


# ══════════════════════════════════════════════════════════════════════════
# MULTI-SIMILARITY LOSS
# ══════════════════════════════════════════════════════════════════════════

class MultiSimilarityLoss(nn.Module):
    """
    Multi-Similarity Loss with General Pair Weighting.
    Reference: Wang et al., "Multi-Similarity Loss with General Pair
    Weighting for Deep Metric Learning", CVPR 2019.

    Combines with supervised contrastive loss for our setting:
    - Self-similarity: anchor-pos pairs
    - Negative similarity: anchor-hard_neg & anchor-easy_neg pairs
    """

    def __init__(self, temperature=0.07, alpha=2.0, beta=50.0, base=0.5):
        super().__init__()
        self.temperature = temperature
        self.alpha = alpha      # positive pair weighting
        self.beta = beta        # negative pair weighting
        self.base = base        # threshold

    def forward(self, embeddings, labels):
        """
        Args:
            embeddings: (B, D) normalized embeddings
            labels: (B,) integer labels (same label = same problem class)
        """
        B = embeddings.shape[0]
        device = embeddings.device

        # Cosine similarity matrix
        sim_mat = torch.matmul(embeddings, embeddings.T) / self.temperature

        # Mask: same label = positive
        labels = labels.unsqueeze(0)
        pos_mask = (labels == labels.T).float()
        neg_mask = 1.0 - pos_mask
        # Remove self
        pos_mask.fill_diagonal_(0)

        # Multi-similarity weighting
        # Positive pairs: weight by hardest positive
        pos_sim = sim_mat * pos_mask
        hardest_pos = pos_sim.max(dim=1, keepdim=True)[0]
        pos_weight = torch.exp(self.alpha * (sim_mat - hardest_pos)) * pos_mask

        # Negative pairs: weight by hardest negative
        neg_sim = sim_mat * neg_mask - 1e9 * pos_mask  # mask out positives
        hardest_neg = neg_sim.max(dim=1, keepdim=True)[0]
        neg_weight = torch.exp(self.beta * (sim_mat - hardest_neg)) * neg_mask

        # InfoNCE-style loss
        numerator = (pos_weight * sim_mat).sum(dim=1)
        denominator = numerator + (neg_weight * sim_mat).sum(dim=1)

        loss = -torch.log(numerator / (denominator + 1e-8)).mean()
        return loss


# ══════════════════════════════════════════════════════════════════════════
# SUPERVISED CONTRASTIVE LOSS
# ══════════════════════════════════════════════════════════════════════════

class SupConLoss(nn.Module):
    """Supervised Contrastive Loss (Khosla et al., NeurIPS 2020)."""

    def __init__(self, temperature=0.07):
        super().__init__()
        self.temperature = temperature

    def forward(self, features, labels):
        """
        Args:
            features: (B, D) normalized feature vectors
            labels: (B,) integer labels
        """
        B = features.shape[0]
        device = features.device

        if B < 2:
            return torch.tensor(0.0, device=device, requires_grad=True)

        # Cosine similarity
        sim = torch.div(torch.matmul(features, features.T), self.temperature)

        # Mask for positives
        labels = labels.contiguous().view(-1, 1)
        mask = torch.eq(labels, labels.T).float().to(device)
        mask.fill_diagonal_(0)

        # For numerical stability
        sim_max, _ = torch.max(sim, dim=1, keepdim=True)
        sim = sim - sim_max.detach()

        # Compute log_prob
        exp_sim = torch.exp(sim) * (1 - mask)  # exclude self
        log_prob = sim - torch.log(exp_sim.sum(dim=1, keepdim=True) + 1e-8)

        # Mean over positives
        mean_log_prob_pos = (mask * log_prob).sum(dim=1) / (mask.sum(dim=1) + 1e-8)

        return -mean_log_prob_pos.mean()


# ══════════════════════════════════════════════════════════════════════════
# COMBINED LOSS
# ══════════════════════════════════════════════════════════════════════════

class CombinedLoss(nn.Module):
    """SupCon + MultiSimilarity loss, weighted sum."""

    def __init__(self, temperature=0.07, supcon_weight=1.0, ms_weight=0.3):
        super().__init__()
        self.supcon = SupConLoss(temperature)
        self.ms = MultiSimilarityLoss(temperature)
        self.supcon_w = supcon_weight
        self.ms_w = ms_weight

    def forward(self, embeddings, labels):
        l_supcon = self.supcon(embeddings, labels)
        l_ms = self.ms(embeddings, labels)
        return self.supcon_w * l_supcon + self.ms_w * l_ms, {
            "supcon": l_supcon.item(),
            "ms": l_ms.item(),
        }


# ══════════════════════════════════════════════════════════════════════════
# TRAINER
# ══════════════════════════════════════════════════════════════════════════

class PEETrainer:
    """Trains Problem Essence Embedding with contrastive learning."""

    def __init__(self, config=None):
        self.config = config or CONFIG
        self.device = self.config["device"]

        # Build base model
        print(f"Loading base model: {self.config['base_model']}")
        word_embedding_model = models.Transformer(
            self.config["base_model"],
            max_seq_length=self.config["max_seq_length"],
        )
        pooling_model = models.Pooling(
            word_embedding_model.get_word_embedding_dimension(),
            pooling_mode="mean",
        )
        self.model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        self.model.to(self.device)

        self.criterion = CombinedLoss(
            temperature=self.config["temperature"],
            supcon_weight=1.0,
            ms_weight=0.3,
        )

    def prepare_data(self):
        """Generate training data and dataloader."""
        print("Generating training descriptions...")
        generator = ProblemDescriptionGenerator(
            num_augmentations=self.config["num_augmentations_per_problem"],
            skeleton_conditioning=self.config["skeleton_conditioning"],
        )
        data = generator.generate_all()
        print(f"  Total training descriptions: {len(data)}")

        # Save descriptions for reproducibility
        desc_path = os.path.join(DATA_DIR, "pee_training_descriptions.json")
        with open(desc_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {desc_path}")

        return data

    def collate_fn(self, batch):
        """Custom collate: flatten anchor/positive/negatives."""
        anchors = [b["anchor"] for b in batch]
        positives = [b["positive"] for b in batch]
        # Include hard negatives and easy negatives
        all_neg = []
        for b in batch:
            all_neg.extend(b["hard_negatives"])
            all_neg.append(b["easy_negative"])

        texts = anchors + positives + all_neg
        # Labels: 0..B-1 for anchors, same for positives, unique for negatives
        B = len(batch)
        labels = list(range(B)) + list(range(B)) + list(range(B, B + len(all_neg)))

        return {"texts": texts, "labels": torch.tensor(labels)}

    def train(self, data=None, num_epochs=None):
        """Main training loop."""
        if data is None:
            data = self.prepare_data()
        if num_epochs is None:
            num_epochs = self.config["num_epochs"]

        dataset = ContrastiveProblemDataset(
            data, num_hard_negatives=self.config["num_hard_negatives_per_batch"]
        )
        dataloader = DataLoader(
            dataset,
            batch_size=self.config["batch_size"],
            shuffle=True,
            collate_fn=self.collate_fn,
            num_workers=0,
        )

        # Optimizer
        optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=self.config["learning_rate"],
            weight_decay=0.01,
        )
        total_steps = len(dataloader) * num_epochs
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=total_steps)

        print(f"\nTraining PEE for {num_epochs} epochs on {self.device}")
        print(f"  Batch size: {self.config['batch_size']}")
        print(f"  Training examples: {len(dataset)}")
        print(f"  Steps per epoch: {len(dataloader)}")

        self.model.train()
        global_step = 0
        best_loss = float("inf")
        loss_history = []

        for epoch in range(num_epochs):
            epoch_loss = 0.0
            epoch_supcon = 0.0
            epoch_ms = 0.0
            pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{num_epochs}")

            for batch in pbar:
                texts = batch["texts"]
                labels = batch["labels"].to(self.device)

                # Encode
                embeddings = self.model.encode(
                    texts,
                    convert_to_tensor=True,
                    show_progress_bar=False,
                    batch_size=self.config["batch_size"],
                )
                embeddings = F.normalize(embeddings, p=2, dim=1)

                # Loss
                loss, loss_components = self.criterion(embeddings, labels)

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()

                epoch_loss += loss.item()
                epoch_supcon += loss_components["supcon"]
                epoch_ms += loss_components["ms"]
                global_step += 1

                pbar.set_postfix({
                    "loss": f"{loss.item():.4f}",
                    "supcon": f"{loss_components['supcon']:.4f}",
                    "lr": f"{scheduler.get_last_lr()[0]:.2e}",
                })

            avg_loss = epoch_loss / len(dataloader)
            avg_supcon = epoch_supcon / len(dataloader)
            avg_ms = epoch_ms / len(dataloader)
            loss_history.append({
                "epoch": epoch + 1,
                "loss": avg_loss,
                "supcon": avg_supcon,
                "ms": avg_ms,
            })

            print(f"  Epoch {epoch+1}: loss={avg_loss:.4f}, supcon={avg_supcon:.4f}, ms={avg_ms:.4f}")

            if avg_loss < best_loss:
                best_loss = avg_loss
                self.save("best")
                print(f"  → Best model saved (loss={best_loss:.4f})")

        # Save final
        self.save("final")
        # Save loss history
        history_path = os.path.join(RESULTS_DIR, "pee_training_loss.json")
        with open(history_path, "w") as f:
            json.dump(loss_history, f, indent=2)
        print(f"\nTraining complete. Best loss: {best_loss:.4f}")
        print(f"Model saved: {MODEL_DIR}/")

        return loss_history

    def save(self, tag="final"):
        """Save model."""
        path = os.path.join(MODEL_DIR, tag)
        os.makedirs(path, exist_ok=True)
        self.model.save(path)
        # Save config
        cfg_path = os.path.join(path, "training_config.json")
        with open(cfg_path, "w") as f:
            json.dump(self.config, f, indent=2, default=str)

    @classmethod
    def load(cls, tag="best"):
        """Load a trained PEE model."""
        path = os.path.join(MODEL_DIR, tag)
        if not os.path.exists(path):
            raise FileNotFoundError(f"No saved model at {path}. Train first.")
        model = SentenceTransformer(path)
        trainer = cls()
        trainer.model = model
        trainer.model.to(trainer.device)
        return trainer

    def encode(self, texts: List[str], batch_size=32):
        """Encode texts to PEE embeddings."""
        self.model.eval()
        with torch.no_grad():
            embs = self.model.encode(
                texts,
                convert_to_tensor=True,
                batch_size=batch_size,
                show_progress_bar=False,
            )
        return F.normalize(embs, p=2, dim=1)


# ══════════════════════════════════════════════════════════════════════════
# ONTOLOGY INDEX BUILDER
# ══════════════════════════════════════════════════════════════════════════

def build_ontology_index(trainer: PEETrainer, skeleton_conditioning=True):
    """Pre-compute PEE embeddings for all ontology entries."""
    print("Building ontology index...")
    ontology_texts = []
    ontology_ids = []

    for prob_id, onto in ONTOLOGY.items():
        text = onto["canonical_description"]
        if skeleton_conditioning:
            skeleton = onto.get("topological_skeleton", "")
            text = f"[Topological Structure: {skeleton}] {text}"
        ontology_texts.append(text)
        ontology_ids.append(prob_id)

    embeddings = trainer.encode(ontology_texts)
    # Convert to numpy for FAISS-compatible storage
    emb_np = embeddings.cpu().numpy()

    index = {
        "problem_ids": ontology_ids,
        "embeddings": emb_np.tolist(),
        "metadata": [{"name": ONTOLOGY[pid]["name"], "family": ONTOLOGY[pid]["family"]}
                      for pid in ontology_ids],
    }

    index_path = os.path.join(MODEL_DIR, "ontology_index.json")
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
    print(f"Ontology index saved: {index_path} ({len(ontology_ids)} entries)")

    return index


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train PEE model")
    parser.add_argument("--epochs", type=int, default=CONFIG["num_epochs"],
                        help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=CONFIG["batch_size"])
    parser.add_argument("--lr", type=float, default=CONFIG["learning_rate"])
    parser.add_argument("--no-skeleton", action="store_true",
                        help="Disable skeleton conditioning")
    parser.add_argument("--device", type=str, default=CONFIG["device"])
    args = parser.parse_args()

    config = {**CONFIG}
    config["num_epochs"] = args.epochs
    config["batch_size"] = args.batch_size
    config["learning_rate"] = args.lr
    config["skeleton_conditioning"] = not args.no_skeleton
    config["device"] = args.device

    trainer = PEETrainer(config)
    data = trainer.prepare_data()
    loss_history = trainer.train(data=data, num_epochs=args.epochs)
    build_ontology_index(trainer, skeleton_conditioning=config["skeleton_conditioning"])
    print("Done!")
