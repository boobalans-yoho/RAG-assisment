from app.evaluation import hit_at_k


def test_hit_at_k_success():
    results = [
        {"id": "doc1"},
        {"id": "doc2"},
        {"id": "doc3"}
    ]

    relevant_ids = {"doc2"}

    score = hit_at_k(results, relevant_ids, k=3)

    assert score == 1.0


def test_hit_at_k_failure():
    results = [
        {"id": "doc1"},
        {"id": "doc2"}
    ]

    relevant_ids = {"doc5"}

    score = hit_at_k(results, relevant_ids, k=2)

    assert score == 0.0


def test_hit_at_k_respects_k():
    results = [
        {"id": "doc1"},
        {"id": "doc2"},
        {"id": "doc3"}
    ]

    relevant_ids = {"doc3"}

    score = hit_at_k(results, relevant_ids, k=2)

    assert score == 0.0