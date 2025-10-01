from flask import Flask, request, jsonify, render_template
from pinecone import Pinecone
from helper_functions import deduplicate_hits
import json

# Init Pinecone
pc = Pinecone(api_key="pcsk_yMcSm_2J4YaTKzpspLY9ub1T9KW1FvqBLk7LybLvEWfQq921xGwnA8Ld7cQBbPxcYdQBK")
index_name = "query-embeddings"
namespace_name = "summaries"
dense_index = pc.Index(index_name)

# Init Flask
app = Flask(__name__)

with open("disease_links.json", "r") as f:
    disease_links = json.load(f)


@app.route("/")
def home():
    return render_template("UI.html")
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    inheritance_filter = request.args.getlist("inheritance")

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # build inheritance filter
    pinecone_moi_filter = {} # moi is short for mode of inheritance
    if inheritance_filter:
        pinecone_moi_filter = {"inheritance": {"$in": inheritance_filter}}

    # Run semantic search
    results = dense_index.search(
        namespace=namespace_name,
        query={
            "top_k": 50,
            "inputs": {"text": query},
            "filter": pinecone_moi_filter
        }
    )

    #Deduplicate by disease
    hits = results["result"]["hits"]
    unique_hits = deduplicate_hits(hits)
    #print("DEBUG unique_hits type:", type(unique_hits))

    # Format for frontend
    formatted = [
        {
            "id": hit["fields"].get("disease_id", hit["_id"]),   # show disease_id
            "score": round(hit["_score"], 3),
            "chunk_text": hit["fields"]["chunk_text"],
            "url": disease_links.get(hit["fields"].get("disease_id", hit["_id"]), "")
        }
        for hit in unique_hits[:20] #show top 20 unique diseases
    ]

    return jsonify({"query": query, "results": formatted})


if __name__ == "__main__":
    app.run(debug=True)
