from app.citations import extract_citations, validate_citations


def test_extract_citations():
    answer = (
        "Employees receive 18 days of annual leave. "
        "[Source: leave_policy.txt, Page 1]"
    )

    citations = extract_citations(answer)

    assert len(citations) == 1


def test_extract_multiple_citations():
    answer = (
        "[Source: leave_policy.txt, Page 1] "
        "[Source: attendance_policy.txt, Page 1]"
    )

    citations = extract_citations(answer)

    assert len(citations) == 2


def test_invalid_citation():
    answer = "Information [Source: unknown.txt, Page 99]"

    chunks = [
        {
            "metadata": {
                "source": "leave_policy.txt",
                "page": 1
            }
        }
    ]

    result = validate_citations(answer, chunks)

    assert result["valid"] is False
    assert len(result["invalid_citations"]) == 1
    assert result["invalid_citations"][0]["source"] == "unknown.txt"
