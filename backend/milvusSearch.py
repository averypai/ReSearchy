from pymilvus import connections, Collection, AnnSearchRequest, RRFRanker
from pymilvus.model.hybrid import BGEM3EmbeddingFunction

from util import extract_highlight_spans

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


collection_name = "hybrid_search"
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
    search_params = {"metric_type": "BM25", "params": {}}
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

    sparse_search_params = {"metric_type": "BM25", "params": {}}
    sparse_req = AnnSearchRequest(
        [query_sparse_embedding], "sparse_vector", sparse_search_params, limit=limit
    )

    rerank = RRFRanker(60)

    res = col.hybrid_search(
        [sparse_req, dense_req],
        rerank=rerank,
        limit=limit,
        output_fields=["id", "title", "author", "abstract"],
    )[0]
    return res


def display_hybrid_results_as_json(ef, query, collection, sparse_weight=0.7, dense_weight=1.0, limit=5):

    output = ef([query])
    dense_query = output["dense"][0]
    sparse_query = output["sparse"][[0]]  

   

    hits = hybrid_search(collection, dense_query, sparse_query, sparse_weight, dense_weight, limit)

    docs = [hit.entity.get("abstract", "") for hit in hits]
    highlight_infos = extract_highlight_spans(ef, query, docs)

    results = []
    for hit, highlight_info in zip(hits, highlight_infos):
        result = {
            "id": hit.entity.get("id", ""),
            "title": hit.entity.get("title", ""),
            "url": hit.entity.get("link", ""),
            "author": hit.entity.get("author", ""),
            "score": hit.distance,
            "abstract_text": highlight_info["text"],
            "highlights": highlight_info["highlights"]
        }
        results.append(result)

    for r in results:
        print("=" * 60)
        print(f"ID: {r['id']}")
        print(f"Title: {r['title']}")
        print(f"URL: {r['url']}")
        print(f"Author: {r['author']}")
        print(f"Score: {r['score']:.4f}")
        print(f"Abstract: {r['abstract_text']}")
        print(f"Highlights (char indices): {r['highlights']}")
        print("=" * 60)
        print()

    return results  



if __name__ == "__main__":
    query = "Reliable collision avoidance under extreme situations remains a critical challenge for autonomous vehicles. While large language models (LLMs) offer promising reasoning capabilities, their application in safety-critical evasive maneuvers is limited by latency and robustness issues. Even so, LLMs stand out for their ability to weigh emotional, legal, and ethical factors, enabling socially responsible and context-aware collision avoidance. This paper proposes a scenario-aware collision avoidance (SACA) framework for extreme situations by integrating predictive scenario evaluation, data-driven reasoning, and scenario-preview-based deployment to improve collision avoidance decision-making. SACA consists of three key components. First, a predictive scenario analysis module utilizes obstacle reachability analysis and motion intention prediction to construct a comprehensive situational prompt. Second, an online reasoning module refines decision-making by leveraging prior collision avoidance knowledge and fine-tuning with scenario data. Third, an offline evaluation module assesses performance and stores scenarios in a memory bank. Additionally, A precomputed policy method improves deployability by previewing scenarios and retrieving or reasoning policies based on similarity and confidence levels. Real-vehicle tests show that, compared with baseline methods, SACA effectively reduces collision losses in extreme high-risk scenarios and lowers false triggering under complex conditions."

    ### the query containing ID, URL, AUTHOR, SCORE .....
    result = display_hybrid_results_as_json(ef, query, collection, sparse_weight=0.7, dense_weight=1.0, limit=5)
