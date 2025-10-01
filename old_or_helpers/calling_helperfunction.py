from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_yMcSm_2J4YaTKzpspLY9ub1T9KW1FvqBLk7LybLvEWfQq921xGwnA8Ld7cQBbPxcYdQBK")
dense_index = pc.Index("query-embeddings")

# print a preview of the index
from helpers import preview_vector
preview_vector(dense_index, "dystonia-ov-summary-1", namespace="summaries")
