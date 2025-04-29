import json

def doc_text_formatting(ef, query, docs):
    tokenizer = ef.model.tokenizer

    # Encode query tokens
    query_encoding = tokenizer.encode_plus(query, return_offsets_mapping=True, add_special_tokens=True)
    query_tokens = tokenizer.convert_ids_to_tokens(query_encoding["input_ids"][1:-1])  # remove CLS, SEP

    formatted_texts = []

    for doc in docs:
        encoding = tokenizer.encode_plus(doc, return_offsets_mapping=True, add_special_tokens=True)
        doc_tokens = tokenizer.convert_ids_to_tokens(encoding["input_ids"][1:-1])
        offsets = encoding["offset_mapping"][1:-1]

        # Collect matched spans
        highlight_spans = []
        for token, (start, end) in zip(doc_tokens, offsets):
            if token in query_tokens:
                highlight_spans.append((start, end))

        # Merge overlaps
        merged_spans = []
        for start, end in sorted(highlight_spans):
            if merged_spans and start <= merged_spans[-1][1]:
                merged_spans[-1] = (merged_spans[-1][0], max(merged_spans[-1][1], end))
            else:
                merged_spans.append((start, end))

        # Insert HTML tags
        formatted_doc = ""
        last_idx = 0
        for start, end in merged_spans:
            formatted_doc += doc[last_idx:start]
            formatted_doc += "<span style='color:red'>" + doc[start:end] + "</span>"
            last_idx = end
        formatted_doc += doc[last_idx:]
        formatted_texts.append(formatted_doc)

    return formatted_texts



def extract_highlight_spans(ef, query, docs):
    tokenizer = ef.model.tokenizer

    query_encoding = tokenizer.encode_plus(query, return_offsets_mapping=True, add_special_tokens=True)
    query_tokens = tokenizer.convert_ids_to_tokens(query_encoding["input_ids"][1:-1])

    results = []

    for doc in docs:
        encoding = tokenizer.encode_plus(doc, return_offsets_mapping=True, add_special_tokens=True)
        doc_tokens = tokenizer.convert_ids_to_tokens(encoding["input_ids"][1:-1])
        offsets = encoding["offset_mapping"][1:-1]

        highlight_spans = []
        for token, (start, end) in zip(doc_tokens, offsets):
            if token in query_tokens:
                highlight_spans.append((start, end))

        # Merge overlapping spans
        merged_spans = []
        for start, end in sorted(highlight_spans):
            if merged_spans and start <= merged_spans[-1][1]:
                merged_spans[-1] = (merged_spans[-1][0], max(merged_spans[-1][1], end))
            else:
                merged_spans.append((start, end))

        results.append({
            "text": doc,
            "highlights": merged_spans
        })

    return results


def test_segment_max_length(jsonl_path):
    
    max_lengths = {
        "id": 0,
        "title": 0,
        "author": 0,
        "link": 0,
        "time": 0,
        "abstract": 0
    }

    
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            try:
                item = json.loads(line)
                for field in max_lengths.keys():
                    value = item.get(field, "")
                    if isinstance(value, str):
                        max_lengths[field] = max(max_lengths[field], len(value))
            except json.JSONDecodeError:
                print(f"[!] JSON decode error at line {idx}")

    print("result：")
    for field, length in max_lengths.items():
        print(f"{field:<10}: {length}")


if __name__ == "__main__":
    jsonl_path = "../data/data_ai_cl.jsonl"
    test_segment_max_length(jsonl_path)
