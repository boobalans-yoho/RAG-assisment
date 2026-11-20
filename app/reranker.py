
from functools import lru_cache


@lru_cache
def get_reranker():

    from sentence_transformers import CrossEncoder

    return CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )


def rerank(
    query: str,
    chunks: list[dict],
    top_n: int = 5
) -> list[dict]:

    if not chunks:
        return []

    model = get_reranker()

    pairs = [
        (query, chunk["text"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    results = []

    for chunk, score in zip(chunks, scores):

        results.append({
            **chunk,
            "rerank_score": float(score)
        })

    results.sort(
        key=lambda item: item["rerank_score"],
        reverse=True
    )

    return results[:top_n]
