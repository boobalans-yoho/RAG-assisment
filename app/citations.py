
import re


CITATION_PATTERN = re.compile(
    r"\[Source:\s*([^,\]]+),\s*Page\s*(\d+)\]",
    re.IGNORECASE
)


def extract_citations(answer: str) -> list[dict]:

    matches = CITATION_PATTERN.findall(answer)

    citations = []

    for source, page in matches:

        citations.append({
            "source": source.strip(),
            "page": int(page)
        })

    return citations


def validate_citations(
    answer: str,
    retrieved_chunks: list[dict]
) -> dict:

    valid_sources = set()

    for chunk in retrieved_chunks:

        metadata = chunk.get(
            "metadata",
            {}
        )

        valid_sources.add((
            metadata.get("source", "unknown"),
            int(metadata.get("page", 1))
        ))

    citations = extract_citations(answer)

    invalid_citations = []

    for citation in citations:

        citation_key = (
            citation["source"],
            citation["page"]
        )

        if citation_key not in valid_sources:

            invalid_citations.append(citation)

    return {
        "citations": citations,
        "invalid_citations": invalid_citations,
        "valid": (
            len(citations) > 0
            and len(invalid_citations) == 0
        )
    }
