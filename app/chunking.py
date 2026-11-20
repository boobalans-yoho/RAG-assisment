
import hashlib
import re


def generate_chunk_id(
    source: str,
    page: int,
    chunk_index: int,
    text: str
) -> str:

    content = f"{source}|{page}|{chunk_index}|{text}"

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def chunk_text(
    text: str,
    source: str,
    page: int = 1,
    chunk_size: int = 180,
    overlap: int = 30
) -> list[dict]:

    words = re.findall(r"\S+", text)

    chunks = []

    start = 0
    index = 0

    while start < len(words):

        end = min(start + chunk_size, len(words))

        chunk_content = " ".join(words[start:end])

        chunk_id = generate_chunk_id(
            source,
            page,
            index,
            chunk_content
        )

        chunks.append({
            "id": chunk_id,
            "text": chunk_content,
            "metadata": {
                "source": source,
                "page": page,
                "chunk_index": index
            }
        })

        if end >= len(words):
            break

        start = end - overlap
        index += 1

    return chunks


def split_documents(
    documents: list[dict],
    chunk_size: int = 180,
    overlap: int = 30
) -> list[dict]:

    all_chunks = []

    for document in documents:

        chunks = chunk_text(
            text=document["text"],
            source=document["source"],
            page=document.get("page", 1),
            chunk_size=chunk_size,
            overlap=overlap
        )

        all_chunks.extend(chunks)

    return all_chunks
