from pathlib import Path

from pypdf import PdfReader

from app.rag.chroma_client import collection

def extract_text_from_pdf(
    pdf_path: str
):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def chunk_text(
    text: str,
    chunk_size: int = 1000
):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks

def ingest_pdf(
    pdf_path: str
):

    text = extract_text_from_pdf(
        pdf_path
    )

    chunks = chunk_text(
        text
    )

    filename = (
        Path(pdf_path).stem
    )

    for idx, chunk in enumerate(chunks):

        collection.add(
            ids=[
            f"{filename}_{idx}"
        ],

        documents=[
            chunk
        ],

        metadatas=[
            {
                "source": filename
            }
        ]
    )

    print(
        f"Ingested {len(chunks)} chunks"
    )