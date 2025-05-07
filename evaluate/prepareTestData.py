import os
import json
import feedparser
import urllib.request
from datetime import datetime
from time import sleep

# Configuration
base_url = "http://export.arxiv.org/api/query?"
results_per_iteration = 50
wait_time = 5  # seconds

output_dir = "TestData"
os.makedirs(output_dir, exist_ok=True)

def fetch_arxiv_data(search_query, total_results, output_file, start_index=0):
    with open(output_file, "w", encoding="utf-8") as output:
        for i in range(start_index, total_results, results_per_iteration):
            query = f"search_query={search_query}&start={i}&max_results={results_per_iteration}"
            full_url = base_url + query

            try:
                with urllib.request.urlopen(full_url) as url:
                    response = url.read()
                feed = feedparser.parse(response)

                for entry in feed.entries:
                    try:
                        authors = ", ".join(author.name for author in entry.authors)
                    except AttributeError:
                        authors = entry.author

                    data = {
                        "author": authors,
                        "abstract": entry.summary,
                        "time": entry.updated,
                        "link": entry.link,
                        "id": entry.link.replace("http://arxiv.org/abs/", ""),
                        "title": entry.title,
                    }

                    json.dump(data, output, ensure_ascii=False)
                    output.write("\n")

                if i + results_per_iteration < total_results:
                    print(f"Fetched {i + results_per_iteration} entries. Sleeping {wait_time} seconds...")
                    sleep(wait_time)
            except Exception as e:
                print(f"Failed at index {i}: {e}")
                break

# Parameters for pools
# Ground truth pool: recent cs.CL papers (2023–2024)
gt_query = "cat:cs.CL+AND+submittedDate:[202301010000+TO+202404010000]"
gt_output_file = os.path.join(output_dir, "ground_truth_pool.jsonl")
fetch_arxiv_data(gt_query, total_results=20, output_file=gt_output_file)

# Negative pool: older non-cs.CL papers (2021–2022)
neg_query = "cat:(cs.LG+OR+cs.AI+OR+cs.SY+OR+cs.DC)+AND+submittedDate:[202101010000+TO+202201010000]"
neg_output_file = os.path.join(output_dir, "negative_pool.jsonl")
fetch_arxiv_data(neg_query, total_results=1000, output_file=neg_output_file)
