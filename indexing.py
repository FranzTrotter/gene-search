# Import the Pinecone library
from pinecone import Pinecone
import json, time, re

# Define dataset to be used for the vector
used_dataset = 'records.json'

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key="pcsk_yMcSm_2J4YaTKzpspLY9ub1T9KW1FvqBLk7LybLvEWfQq921xGwnA8Ld7cQBbPxcYdQBK")
index_name = "query-embeddings"
namespace_name = "summaries"

# Recreate the index (optional cleanup)
if pc.has_index(index_name):
    pc.delete_index(index_name)

pc.create_index_for_model(
    name=index_name,
    cloud="aws",
    region="us-east-1",
    embed={
        "model":"llama-text-embed-v2",
        "field_map":{"text": "chunk_text"}
    }
)

# upsert data
with open(used_dataset, 'r') as f:
    records = json.load(f)

# Target the index
dense_index = pc.Index(index_name)

# Chunking function
HEADINGS = ["Clinical characteristics",
            "Diagnosis/testing",
            "Management",
            "Genetic counseling"]

# Precompile regex pattern for heading detection
heading_pattern = re.compile(r'(?i)\b(' + '|'.join(map(re.escape, HEADINGS)) + r')\b\s*:?')

def chunk_summary(summary_text, doc_id, inheritance):
    # Split a single summary (one long line of text) into chunks by headings.
    # Falls back to one chunk if no headings are found.
    chunks = []
    matches = list(heading_pattern.finditer(summary_text))

    if not matches:
        return [{
            "_id": f"{doc_id}-summary",
            "disease_id": doc_id,
            "chunk_text": summary_text.strip(),
            "heading": "Summary",
            "inheritance": inheritance
        }]
    
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(summary_text)

        heading = match.group(1).strip()
        content = summary_text[start:end].strip()

        if content:  # skip empty sections
            chunks.append({
                "_id": f"{doc_id}-{heading.lower().replace(' ', '-')}",
                "disease_id": doc_id,
                "heading": heading,
                "chunk_text": content,
                "inheritance": inheritance
            })

    return chunks

# Convert dataset summaries into chunked records
all_chunks = []
for record in records:
    doc_id = record["_id"]
    summary_text = record.get("chunk_text", "")
    inheritance = record.get("inheritance", [])
    all_chunks.extend(chunk_summary(summary_text, doc_id, inheritance))


# Batch size (adjust this depending on payload size — 50 is usually safe)
batch_size = 50 #number of records sent per API call

# Upsert in safe batches
for i in range(0, len(all_chunks), batch_size):
    batch = all_chunks[i:i + batch_size]
    dense_index.upsert_records(namespace=namespace_name, records=batch)
    print(f"Upserted {i // batch_size + 1} / {(len(all_chunks) + batch_size - 1) // batch_size}")
    time.sleep(4)

#quick test (checks, if my Pinecone client has the new method available since switching form upsert to upsert_records)
print("Has method:", hasattr(dense_index, "upsert_records"))  # should be True

# Wait for the upserted vectors to be indexed
time.sleep(10)

# View stats for the index
stats = dense_index.describe_index_stats()
print(stats)