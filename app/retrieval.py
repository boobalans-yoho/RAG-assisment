
from .vector_store import VectorStore


def retrieve(
    query: str,
    store: VectorStore,
    k: int = 4,
    department: str | None = None,
    year: int | None = None
) -> list[dict]:

    filters = {
        "department": department,
        "year": year
    }

    filters = {
        key: value
        for key, value in filters.items()
        if value is not None
    }

    return store.search(
        query=query,
        k=k,
        filters=filters or None
    )
