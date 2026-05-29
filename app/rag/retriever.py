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

def retrieve_from_source(
    query: str,
    source: str,
    n_results: int = 3
):

    results = collection.query(

        query_texts=[query],

        where={
            "source": source
        },

        n_results=n_results
    )

    return results["documents"][0]

def get_available_sources():
    
    results = collection.get(
        include=["metadatas"]
    )

    sources = set()

    for metadata in results["metadatas"]:

        sources.add(
            metadata["source"]
        )

    return list(sources)