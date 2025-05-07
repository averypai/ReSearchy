# storage_windows_final.py

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import torch
import json
import numpy as np
import scipy.sparse
from tqdm import tqdm
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from pymilvus.model.hybrid import BGEM3EmbeddingFunction

import os

MILVUS_URI = ""
MILVUS_PORT = ""
MILVUS_USER = ""
MILVUS_PASSWORD = ""

COLLECTION_NAME = "TestDataSet"



connections.connect(
    uri=MILVUS_URI,
    user=MILVUS_USER,
    password=MILVUS_PASSWORD,
    secure=True
)

device = "cuda" if (torch.cuda.is_available()) else "cpu"

print(device)
if device != "cuda":
    exit()


ef = BGEM3EmbeddingFunction(device=device, use_fp16=(device=="cuda"))
dense_dim = ef.dim["dense"]

def sparse_tensor_batch_to_list_of_dicts(tensor):
    tensor = tensor.tocoo()
    results = [{} for _ in range(tensor.shape[0])]
    for i, j, v in zip(tensor.row, tensor.col, tensor.data):
        results[i][j] = float(v)
    return results



def load_jsonl_new():
    path1 = 'TestData/negative_pool.jsonl'
    path2 = 'TestData/ground_truth_augmented_fluent.jsonl'
    data = []
    with open(path1, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    with open(path2, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def create_collection(name):
    if utility.has_collection(name):
        collection = Collection(name)
        print(f"Collection '{name}' already exists.")
        return collection
    
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="author", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="time", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="abstract", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=dense_dim),
        FieldSchema(name="sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
    ]
    schema = CollectionSchema(fields, description="Hybrid dense+sparse collection")
    collection = Collection(name, schema)
    return collection


def insert_batch(collection, batch_data, dense_list, sparse_list, offset):
    ids = []
    titles = []
    authors = []
    links = []
    times = []
    abstracts = []

    for idx, item in enumerate(batch_data):
   
        raw_id = item.get("id", "").strip()
        if not raw_id:
            raise ValueError(f"Missing or empty id at line {idx}")
        ids.append(raw_id)
        titles.append(item.get("title", "").strip())
        authors.append(item.get("author", "").strip()[:500])
        links.append(item.get("link", "").strip())
        times.append(item.get("time", "").strip())
        abstracts.append(item.get("abstract", ""))

    dense_batch = [dense_list[offset+idx].tolist() for idx in range(len(batch_data))]
    sparse_batch = sparse_tensor_batch_to_list_of_dicts(sparse_list[offset:offset+len(batch_data)])

    collection.insert([
        ids, titles, authors, links, times, abstracts,
        dense_batch, sparse_batch
    ])


    collection.create_index(
        field_name="sparse_vector",
        index_params={
            "index_type": "SPARSE_INVERTED_INDEX",
            "metric_type": "IP"
        }
    )


    collection.create_index(
        field_name="dense_vector",
        index_params={
            "index_type": "AUTOINDEX",
            "metric_type": "COSINE"
        }
    )

  
    collection.load()


def main():

    data = load_jsonl_new()

    
    texts = [item.get("abstract", "") for item in data]
    embeds = ef(texts)
    dense_list = embeds["dense"]
    sparse_list = embeds["sparse"]

   
    collection = create_collection(COLLECTION_NAME)

    batch_size = 30
    num_batches = (len(data) + batch_size - 1) // batch_size


    for i in tqdm(range(num_batches)):
        batch = data[i*batch_size : (i+1)*batch_size]
        insert_batch(collection, batch, dense_list, sparse_list, offset=i*batch_size)

    collection.load()
    print("All data inserted and collection loaded!")

if __name__ == "__main__":
    main()
