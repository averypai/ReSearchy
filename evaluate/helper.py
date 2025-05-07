import math
import json

def precision_at_k(retrieved_ids, ground_truth_ids, k):
    retrieved_top_k = retrieved_ids[:k]
    hits = [1 if rid in ground_truth_ids else 0 for rid in retrieved_top_k]
    return sum(hits) / k

def recall_at_k(retrieved_ids, ground_truth_ids, k):
    hits = [1 if rid in ground_truth_ids else 0 for rid in retrieved_ids[:k]]
    return sum(hits) / len(ground_truth_ids)

def ndcg_at_k(retrieved_ids, ground_truth_ids, k):
    def dcg(scores):
        return sum(score / math.log2(idx + 2) for idx, score in enumerate(scores))

    relevance = [1 if rid in ground_truth_ids else 0 for rid in retrieved_ids[:k]]
    dcg_score = dcg(relevance)
    ideal_relevance = sorted(relevance, reverse=True)
    idcg_score = dcg(ideal_relevance)
    return dcg_score / idcg_score if idcg_score > 0 else 0.0

def mrr(retrieved_ids, ground_truth_ids):
    for idx, rid in enumerate(retrieved_ids):
        if rid in ground_truth_ids:
            return 1 / (idx + 1)
    return 0.0

def ndcg_at_k_order_sensitive(retrieved_ids, ground_truth_ids, k):
 
    def relevance_score(gid):
        if "_level" in gid:
            try:
                level = int(gid.split("_level")[1])
                return 6 - level if 1 <= level <= 5 else 0
            except:
                return 0
        return 0

    gt_relevance = {gid: relevance_score(gid) for gid in ground_truth_ids}

    relevance = [gt_relevance.get(rid, 0) for rid in retrieved_ids[:k]]
    ideal = sorted(gt_relevance.values(), reverse=True)[:k]

    def dcg(scores):
        return sum(score / math.log2(i + 2) for i, score in enumerate(scores))

    dcg_score = dcg(relevance)
    idcg_score = dcg(ideal)

    return dcg_score / idcg_score if idcg_score > 0 else 0.0


def load_positive_queries(path):

    queries = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            queries[record["id"]] = record["abstract"]
    return queries

def build_ground_truth_map(path):

    gt_map = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            base_id = record["id"].split("_level")[0]
            gt_map.setdefault(base_id, []).append(record["id"])
    return gt_map
