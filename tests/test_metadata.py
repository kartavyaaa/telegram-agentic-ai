from app.rag.chroma_client import collection

results = collection.get(
    limit=5,
    include=["metadatas"]
)

print(results)