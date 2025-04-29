import urllib.request
import time
import feedparser
import json

# Base api query url
base_url = "http://export.arxiv.org/api/query?"

# Search parameters
search_query = "cat:cs.CL+AND+submittedDate:[202201010600+TO+202504010600]"
start = 550  # start at the first result
total_results = 10000  # want 10000 total results
results_per_iteration = 50  # 5 results at a time
wait_time = 5  # number of seconds to wait between calls

with open("data_latest.jsonl", "a") as output:
    for i in range(start, total_results, results_per_iteration):
        # Properly format the query URL
        query = (
            f"search_query={search_query}&start={i}&max_results={results_per_iteration}"
        )
        full_url = base_url + query

        # Perform a GET request using urllib
        with urllib.request.urlopen(full_url) as url:
            response = url.read()

        # Parse the response using feedparser
        feed = feedparser.parse(response)

        # Run through each entry, and print out information
        for entry in feed.entries:
            try:
                authors = ", ".join(author.name for author in entry.authors)
            except AttributeError:
                # Fall back to single author if authors list isn't available
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

        # Sleep before making the next API call
        if i + results_per_iteration < total_results:
            print(f"Sleeping for {wait_time} seconds")
            time.sleep(wait_time)
