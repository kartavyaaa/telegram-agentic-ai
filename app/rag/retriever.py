from app.rag.chroma_client import collection

def retrieve_context(
    query: str,
    n_results: int = 3
):

    results = collection.query(

        query_texts=[
            query
        ],

        n_results=n_results
    )

    return results["documents"][0]