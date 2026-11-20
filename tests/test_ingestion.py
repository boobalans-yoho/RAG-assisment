from app.ingestion import build_chunks


def test_build_chunks_from_txt(tmp_path):
    file_path = tmp_path / "test_policy.txt"
    file_path.write_text(
        "Employees receive 18 days of annual leave.",
        encoding="utf-8"
    )

    chunks = build_chunks(tmp_path)

    assert len(chunks) > 0
    assert "annual leave" in chunks[0]["text"].lower()


def test_chunk_has_stable_id(tmp_path):
    file_path = tmp_path / "policy.txt"
    file_path.write_text("Company HR policy information.", encoding="utf-8")

    first = build_chunks(tmp_path)
    second = build_chunks(tmp_path)

    assert first[0]["id"] == second[0]["id"]


def test_empty_directory_returns_empty(tmp_path):
    chunks = build_chunks(tmp_path)

    assert chunks == []