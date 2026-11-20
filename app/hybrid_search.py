
from collections import defaultdict

from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:

    return text.lower().split()


class HybridRetriever:

    def __init__(
        self,
        chunks: list[dict],
        vector_store
    ):

        self.chunks = chunks

        self.vector_store = vector_store

        self.bm25 = None

        if chunks:

            tokenized = [
                tokenize(chunk["text"])
                for chunk in chunks
            ]

            self.bm25 = BM25Okapi(tokenized)

    def bm25_search(
        self,
        query: str,
        k: int = 10
    ) -> list[dict]:

        if self.bm25 is None:
            return []

        scores = self.bm25.get_scores(
            tokenize(query)
        )

        indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:k]

        return [
            {
                **self.chunks[i],
                "score": float(scores[i])
            }
            for i in indices
        ]

    def vector_search(
        self,
        query: str,
        k: int = 10
    ) -> list[dict]:

        return self.vector_store.search(
            query,
            k
        )

    @staticmethod
    def reciprocal_rank_fusion(
        *result_lists,
        constant: int = 60
    ) -> list[dict]:

        scores = defaultdict(float)

        documents = {}

        for results in result_lists:

            for rank, document in enumerate(
                results,
                start=1
            ):

                doc_id = document["id"]

                scores[doc_id] += (
                    1 / (constant + rank)
                )

                documents[doc_id] = document

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            {
                **documents[doc_id],
                "rrf_score": score
            }
            for doc_id, score in ranked
        ]

    def search(
        self,
        query: str,
        k: int = 5
    ) -> list[dict]:

        bm25_results = self.bm25_search(
            query,
            k=50
        )

        vector_results = self.vector_search(
            query,
            k=50
        )

        hybrid_results = self.reciprocal_rank_fusion(
            bm25_results,
            vector_results
        )

        return hybrid_results[:k]
