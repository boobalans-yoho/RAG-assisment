
from functools import lru_cache

import numpy as np

from .config import get_settings


@lru_cache
def get_embedding_model():

    from sentence_transformers import SentenceTransformer

    settings = get_settings()

    model = SentenceTransformer(
        settings.EMBEDDING_MODEL
    )

    return model


def embed_texts(
    texts: list[str]
) -> np.ndarray:

    if not texts:

        return np.empty(
            (0, 384),
            dtype="float32"
        )

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return np.asarray(
        embeddings,
        dtype="float32"
    )


def embed_query(
    query: str
) -> np.ndarray:

    return embed_texts([query])[0]
