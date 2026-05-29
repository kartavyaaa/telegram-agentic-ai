from app.rag.retriever import (
    retrieve_context
)

results = retrieve_context(
    "some question"
)

print(results)