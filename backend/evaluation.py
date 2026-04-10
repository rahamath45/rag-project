from dataset import dataset
import requests
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# --- collect RAG outputs ---
questions, answers, contexts, ground_truths = [], [], [], []

for item in dataset:
    q = item["question"]
    res = requests.get(
        "http://127.0.0.1:8002/ask",
        params={"question": q}
    ).json()

    a = res.get("answer", "")
    ctx = res.get("context", "")

    questions.append(q)
    answers.append(a)
    contexts.append([ctx])
    ground_truths.append(item["ground_truth"])

# --- simple local evaluation ---
def get_embedding_local(text):
    import requests
    resp = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    return resp.json()["embedding"]

def word_overlap_score(pred, truth):
    pred_words = set(pred.lower().split())
    truth_words = set(truth.lower().split())
    if not pred_words or not truth_words:
        return 0.0
    intersection = pred_words & truth_words
    return len(intersection) / len(truth_words)

print(f"{'Question':<30} {'Overlap':<10} {'Embedding Sim':<15}")
print("-" * 55)

for q, a, gt in zip(questions, answers, ground_truths):
    overlap = word_overlap_score(a, gt)
    a_emb = np.array(get_embedding_local(a)).reshape(1, -1)
    gt_emb = np.array(get_embedding_local(gt)).reshape(1, -1)
    emb_sim = cosine_similarity(a_emb, gt_emb)[0][0]
    print(f"{q:<30} {overlap:<10.3f} {emb_sim:<15.3f}")

# summary
overlaps = [word_overlap_score(a, gt) for a, gt in zip(answers, ground_truths)]
embs_a = [np.array(get_embedding_local(a)).reshape(1, -1) for a in answers]
embs_gt = [np.array(get_embedding_local(gt)).reshape(1, -1) for gt in ground_truths]
emb_sims = [cosine_similarity(ea, eg)[0][0] for ea, eg in zip(embs_a, embs_gt)]

print(f"\nAverage Overlap Score:    {np.mean(overlaps):.3f}")
print(f"Average Embedding Sim:    {np.mean(emb_sims):.3f}")
