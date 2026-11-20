
import json
from pathlib import Path

import numpy as np

from .embeddings import embed_texts, embed_query


class VectorStore:

    def __init__(self, index_dir="data/processed"):

        self.path = Path(index_dir)

        self.path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.chunks = []

        self.vectors = np.empty(
            (0, 384),
            dtype="float32"
        )

        self.index = None

    def load(self):

        chunks_file = self.path / "chunks.json"
        vectors_file = self.path / "vectors.npy"

        if chunks_file.exists() and vectors_file.exists():

            self.chunks = json.loads(
                chunks_file.read_text(
                    encoding="utf-8"
                )
            )

            self.vectors = np.load(
                vectors_file
            ).astype("float32")

            self._build_index()

        return self

    def _build_index(self):

        if not len(self.vectors):
            self.index = None
            return

        try:

            import faiss

            self.index = faiss.IndexFlatIP(
                self.vectors.shape[1]
            )

            self.index.add(self.vectors)

        except ImportError:

            self.index = None

    def _save(self):

        chunks_file = self.path / "chunks.json"

        chunks_file.write_text(
            json.dumps(
                self.chunks,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        np.save(
            self.path / "vectors.npy",
            self.vectors
        )

    def add_chunks(self, chunks: list[dict]) -> int:

        existing_ids = {
            chunk["id"] for chunk in self.chunks
        }

        new_chunks = [
            chunk for chunk in chunks
            if chunk["id"] not in existing_ids
        ]

        if not new_chunks:
            return 0

        vectors = embed_texts([
            chunk["text"]
            for chunk in new_chunks
        ])

        self.chunks.extend(new_chunks)

        if len(self.vectors) == 0:

            self.vectors = vectors

        else:

            self.vectors = np.vstack([
                self.vectors,
                vectors
            ])

        self._save()

        self._build_index()

        return len(new_chunks)

    def search(
        self,
        query: str,
        k: int = 4,
        filters: dict | None = None
    ) -> list[dict]:

        if not self.chunks:
            return []

        query_vector = embed_query(query)

        if self.index is not None:

            scores, indices = self.index.search(
                query_vector.reshape(1, -1),
                len(self.chunks)
            )

            ranked = [
                (int(index), float(score))
                for index, score in zip(
                    indices[0],
                    scores[0]
                )
                if index >= 0
            ]

        else:

            scores = self.vectors @ query_vector

            ranked = sorted(
                enumerate(scores.tolist()),
                key=lambda item: item[1],
                reverse=True
            )

        results = []

        for index, score in ranked:

            chunk = self.chunks[index]

            metadata = chunk.get("metadata", {})

            if filters:

                mismatch = any(
                    metadata.get(key) != value
                    for key, value in filters.items()
                    if value is not None
                )

                if mismatch:
                    continue

            results.append({
                **chunk,
                "score": score
            })

            if len(results) >= k:
                break

        return results
