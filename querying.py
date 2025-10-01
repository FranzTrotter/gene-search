import cohere
from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_yMcSm_2J4YaTKzpspLY9ub1T9KW1FvqBLk7LybLvEWfQq921xGwnA8Ld7cQBbPxcYdQBK")
co = cohere.Client("YYEK15kl40DMFHrcMSCMs2zy74D3WhpPZpiXaXQQ")

# Target the existing index
index_name = "query-embeddings"
namespace_name = "summaries"
index = pc.Index(index_name)

# Define the query
query = input("Please give your query here: ")

# Filter system
# mortality = "For the mortality filter please choose from the following.\nhigh\nlow\nnone\n"
# inheritance = "For the inheritance filter please choose from the following.\nautosomal recessive\nautosomal dominant\nnone\n"
# penetrance = "For the penetrance filter please choose from the following.\nhigh\nlow\nvariable\nnone\n"

# Search the dense index
results = index.search(
    namespace = namespace_name,
    query={
        "top_k": 25,   #this should always be higher than the actual number of hits one wants to give the reranker
        "inputs": {'text': query}#,
        # "filter": {"mortality": mortality ,
        #            "penetrance": penetrance ,
        #            "inheritance": inheritance}
        },
    fields=["chunk_text", "inheritance"] #return text&metadata
    # rerank={
    #     "model": "cohere-rerank-3.5",
    #     "top_n": 15, #ADJUSTABLE NUMBER!
    #     "rank_fields": ["chunk_text"]
    # }
)

# Print the results
for hit in results['result']['hits']:
    text = hit["fields"]["chunk_text"][:200].replace("\n", " ") #preview first 200 chars
    inheritance = hit["fields"].get("inheritance", "N/A")
    print(f"id: {hit['_id']}, score: {round(hit['_score'], 3)}, inheritance: {inheritance}, text: {text}...")

# external reranking using Cohere's SDK
# Extract text chunks and corresponding hits
##documents = [hit['fields']['chunk_text'] for hit in dense_results['result']['hits']]
#print(documents)
##original_hits = dense_results['result']['hits']

# Call Cohere's rerank endpoint
# rerank_results = co.rerank(
#     model="cohere-rerank-3.5",
#     query=query,
#     documents=documents,
#     top_n=10  # ADJUSTABLE NUMBER!!
# )

# Map reranked indices back to original hits
##reranked_hits = [original_hits[result.index] for result in rerank_results.results]

# Print top reranked results
## for hit in reranked_hits:
##     print(f"id: {hit['_id']}, score: {round(hit['_score'], 2)}")
#, text: {hit['fields']['chunk_text'][:300]}...

# Search the dense index and rerank results
# reranked_results = dense_index.search(
#     namespace="example-namespace",
#     query={
#         "top_k": 25,
#         "inputs": {
#             'text': query
#          }
#     },
#     rerank={
#         "model": "cohere-rerank-english-v2.0",
#         "top_n": 10,
#         "rank_fields": ["chunk_text"]
#     }  
# )

# # Print the reranked results
#for hit in reranked_results['result']['hits']:
#    print(f"id: {hit['_id']}, score: {round(hit['_score'], 2)}, text: {hit['fields']['chunk_text']}, category: {hit['fields']['category']}")