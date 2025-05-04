from pymilvus import connections, Collection, AnnSearchRequest, RRFRanker, WeightedRanker
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


# ef = BGEM3EmbeddingFunction(device="cuda", use_fp16=False)
ef = BGEM3EmbeddingFunction(device="cpu", use_fp16=False)

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
    query = "A common feature of these semantics is that one can always maximize in some sense the set of acceptable arguments"

    ### the query containing ID, URL, AUTHOR, SCORE .....
    result = display_hybrid_results_as_json(ef, query, collection, sparse_weight=0.5, dense_weight=0.5, limit=10)
