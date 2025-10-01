from flask import Flask, request, jsonify, render_template
from pinecone import Pinecone
from helper_functions import deduplicate_hits

# Init Pinecone
pc = Pinecone(api_key="pcsk_yMcSm_2J4YaTKzpspLY9ub1T9KW1FvqBLk7LybLvEWfQq921xGwnA8Ld7cQBbPxcYdQBK")
index_name = "query-embeddings"
namespace_name = "summaries"
dense_index = pc.Index(index_name)

# Init Flask
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Run semantic search
    results = dense_index.search(
        namespace=namespace_name,
        query={
            "top_k": 25,
            "inputs": {"text": query}
        }
    )

    #Deduplicate by disease
    hits = results["result"]["hits"]
    unique_hits = deduplicate_hits(hits)

    # Pich top N from theunique hits for reranking
    top_for_rerank = unique_hits[:10]

    # Integrated rerank using Pinecone search + rerank parameter
    ranked_results = dense_index.search(
        namespace=namespace_name,
        query={
            "top_k": 20,
            "inputs":{"text": query}
        },
        rerank={
            "model": "bge-reranker-v2-m3",
            "top_n": 5,
            "rank_fields": ["chunk_text"]
        },
        fields=["chunk_text"]
    )

    # Deduplicate again after rerank so you don't doube-count diseases
    final_hits = deduplicate_hits(ranked_results["result"]["hits"])

    # Format for frontend
    formatted = []
    for hit in final_hits[:10]:
        formatted.append({
            "id": hit["_id"],
            "score": round(hit["_score"], 3),
            "chunk_text": hit["fields"]["chunk_text"][:300] + "..."  # preview
        })
    
    return jsonify({"query": query, "results": formatted})


if __name__ == "__main__":
    app.run(debug=True)
