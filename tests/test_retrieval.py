
from app.retrieval import retrieve
from app.vector_store import VectorStore
from app.config import settings


def get_test_store():
    store = VectorStore(index_dir=settings.INDEX_DIR)
    store.load()
    return store


def test_retrieve_returns_results():
    store = get_test_store()

    results = retrieve(
        query="annual leave policy",
        store=store,
        k=4
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_retrieve_respects_top_k():
    store = get_test_store()

    results = retrieve(
        query="employee benefits",
        store=store,
        k=2
    )

    assert len(results) <= 2


def test_retrieve_with_department_filter():
    store = get_test_store()

    results = retrieve(
        query="HR employee policy",
        store=store,
        k=4,
        department="HR"
    )

    assert isinstance(results, list)
