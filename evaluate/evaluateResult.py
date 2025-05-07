import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from pymilvus import connections, Collection, AnnSearchRequest, RRFRanker, WeightedRanker
from pymilvus.model.hybrid import BGEM3EmbeddingFunction

import json
import helper



MILVUS_URI = ""
MILVUS_PORT = ""
MILVUS_USER = ""
MILVUS_PASSWORD = ""


connections.connect(
    uri=MILVUS_URI,
    user=MILVUS_USER,
    password=MILVUS_PASSWORD,
    secure=True
)


collection_name = "TestDataSet"
collection = Collection(collection_name)
collection.load()


ef = BGEM3EmbeddingFunction(device="cuda", use_fp16=False)
# ef = BGEM3EmbeddingFunction(device="cpu", use_fp16=False)

def dense_search(col, query_dense_embedding, limit=10):
    search_params = {"metric_type": "COSINE", "params": {}}
    res = col.search(
        [query_dense_embedding],
        anns_field="dense_vector",
        limit=limit,
        output_fields=["id", "title", "author", "abstract"],
        param=search_params,
    )[0]
    return res

def sparse_search(col, query_sparse_embedding, limit=10):
    search_params = {"metric_type": "IP", "params": {}}
    res = col.search(
        [query_sparse_embedding],
        anns_field="sparse_vector",
        limit=limit,
        output_fields=["id", "title", "author", "abstract"],
        param=search_params,
    )[0]
    return res

def hybrid_search(
    col,
    query_dense_embedding,
    query_sparse_embedding,
    sparse_weight=1.0,
    dense_weight=1.0,
    limit=10,
):
    dense_search_params = {"metric_type": "COSINE", "params": {}}
    dense_req = AnnSearchRequest(
        [query_dense_embedding], "dense_vector", dense_search_params, limit=limit
    )

    sparse_search_params = {"metric_type": "IP", "params": {}}
    sparse_req = AnnSearchRequest(
        [query_sparse_embedding], "sparse_vector", sparse_search_params, limit=limit
    )

    # rerank = RRFRanker(60)
    rerank = WeightedRanker(0.5, 0.5)

    res = col.hybrid_search(
        [sparse_req, dense_req],
        rerank=rerank,
        limit=limit,
        output_fields=["id", "title", "author", "abstract"],
    )[0]
    return res



def build_evaluation_tasks(positive_path, augmented_path):
    """
    [
        {
            "query_id": ...,
            "query_text": ...,
            "ground_truth_ids": [...]
        },
        ...
    ]
    """
    query_texts = {}
    with open(positive_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            query_texts[record["id"]] = record["abstract"]

 
    gt_map = {}
    with open(augmented_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if "_level" in record["id"]:
                base_id = record["id"].split("_level")[0]
                gt_map.setdefault(base_id, []).append(record["id"])


    tasks = []
    for qid, text in query_texts.items():
        if qid in gt_map:
            tasks.append({
                "query_id": qid,
                "query_text": text,
                "ground_truth_ids": gt_map[qid]
            })

    return tasks



def evaluate_query(ef, query_id, query_text, ground_truth_ids,
                   sparse_weight=0.7, dense_weight=1.0,
                   max_level=5, limit=5):

    filtered_gt = []
    for gid in ground_truth_ids:
        if "_level" in gid:
            try:
                level_num = int(gid.split("_level")[1])
                if level_num <= max_level:
                    filtered_gt.append(gid)
            except:
                continue

    if not filtered_gt:
        return {
            "query_id": query_id,
            "precision@K": 0,
            "recall@K": 0,
            "ndcg@K": 0,
            "mrr": 0,
            "top_K": 0,
            "retrieved_ids": [],
            "ground_truth_ids": []
        }

    output = ef([query_text])
    dense_query = output["dense"][0]
    sparse_query = output["sparse"][[0]]


    hits = hybrid_search(collection, dense_query, sparse_query, sparse_weight, dense_weight, limit)
    retrieved_ids = [hit.entity.get("id", "") for hit in hits]


    K = min(limit, len(filtered_gt))

    return {
        "query_id": query_id,
        "precision@K": helper.precision_at_k(retrieved_ids, filtered_gt, K),
        "recall@K": helper.recall_at_k(retrieved_ids, filtered_gt, K),
        "ndcg@K": helper.ndcg_at_k_order_sensitive(retrieved_ids, filtered_gt, K),
        "mrr": helper.mrr(retrieved_ids, filtered_gt),
        "top_K": K,
        "retrieved_ids": retrieved_ids,
        "ground_truth_ids": filtered_gt
    }





if __name__ == "__main__":
    # query = "A common feature of these semantics is that one can always maximize in some sense the set of acceptable arguments"

    # ### the query containing ID, URL, AUTHOR, SCORE .....
    # result = EvaluateOnce(ef, query, collection, sparse_weight=0.5, dense_weight=0.5, limit=5)


    count = 0
    choice = 3

    tasks = build_evaluation_tasks("TestData/ground_truth_pool.jsonl", "TestData/ground_truth_augmented_fluent.jsonl")
    
    results = []
    for task in tasks:
        if count > choice:
            break
        else: count += 1

        res = evaluate_query(
            ef=ef,
            query_id=task["query_id"],
            query_text=task["query_text"],
            ground_truth_ids=task["ground_truth_ids"],
            sparse_weight=0.5,
            dense_weight=0.5,
            max_level=4,
            limit=10
        )
        results.append(res)

        print(f"\n[Query ID: {res['query_id']}]")
        print(f"Top-K:      {res['top_K']}")
        print(f"Precision@K: {res['precision@K']:.4f}")
        print(f"Recall@K:    {res['recall@K']:.4f}")
        print(f"NDCG@K:      {res['ndcg@K']:.4f}")
        print(f"MRR:         {res['mrr']:.4f}")
        print(f"Top IDs:     {res['retrieved_ids']}\n")

