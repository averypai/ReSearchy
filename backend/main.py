import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal

from milvusSearch import display_hybrid_results_as_json, ef, collection
from util import extract_highlight_spans

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class CompareRequest(BaseModel):
    query: str
    paper_text: str

class HighlightSpan(BaseModel):
    start: int
    end: int
    category: Literal["concept", "methodology"] = "concept"

class CompareResponse(BaseModel):
    userHighlights: List[HighlightSpan]
    paperHighlights: List[HighlightSpan]

class PaperResult(BaseModel):
    id: str
    title: str
    authors: List[str]
    year: str
    abstract: str
    similarityScore: float
    url: str

class SearchResponse(BaseModel):
    results: List[PaperResult]
    
@app.post("/search", response_model=SearchResponse)
def search_endpoint(req: SearchRequest):
    raw_results = display_hybrid_results_as_json(
        ef=ef,
        query=req.query,
        collection=collection,
        sparse_weight=0.7,
        dense_weight=1.0,
        limit=req.top_k
    )

    results = []
    for r in raw_results:
        results.append({
            "id": r["id"],
            "title": r["title"],
            "authors": r["author"].split(", "),
            "year": "2023",
            "abstract": r["abstract_text"],
            "similarityScore": round(r["score"], 4),
            "url": r["url"] or f"https://arxiv.org/abs/{r['id']}"
        })

    return {"results": results}

@app.post("/compare", response_model=CompareResponse)
def compare_endpoint(req: CompareRequest):
    query = req.query
    paper = req.paper_text

    query_spans = extract_highlight_spans(ef, query, [paper])[0]["highlights"]
    paper_spans = extract_highlight_spans(ef, paper, [query])[0]["highlights"]

    def with_category(spans):
        return [
            {"start": s, "end": e, "category": "concept"} for s, e in spans
        ]

    return {
        "userHighlights": with_category(query_spans),
        "paperHighlights": with_category(paper_spans)
    }