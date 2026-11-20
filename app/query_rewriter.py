
def rewrite_query(question: str) -> list[str]:

    question = question.strip().rstrip("?")

    queries = [
        question,

        f"What does company policy say about {question}?",

        f"What are the rules and requirements for {question}?",

        f"According to the employee handbook, {question}?"
    ]

    return list(dict.fromkeys(queries))


def search_rewritten_queries(
    question: str,
    retriever,
    k: int = 5
) -> list[dict]:

    from .hybrid_search import HybridRetriever

    queries = rewrite_query(question)

    result_lists = []

    for query in queries:

        results = retriever.search(
            query,
            k=50
        )

        result_lists.append(results)

    merged = HybridRetriever.reciprocal_rank_fusion(
        *result_lists
    )

    return merged[:k]
