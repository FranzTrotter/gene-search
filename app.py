from flask import Flask, request, jsonify, render_template
from pinecone import Pinecone
from helper_functions import deduplicate_hits
import json, os

# Init Pinecone
api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
