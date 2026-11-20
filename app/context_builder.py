
import re


def count_tokens(text: str) -> int:

    # Simple approximation.
    # Use tiktoken for exact model token counting.

    return max(
        1,
        len(re.findall(r"\w+|[^\w\s]", text))
    )


def fit_context(
    chunks: list[dict],
    budget: int
) -> list[dict]:

    selected = []

    used_tokens = 0

    if budget <= 0:
        return selected

    for chunk in chunks:

        text = chunk.get("text", "")

        tokens = count_tokens(text)

        if used_tokens + tokens <= budget:

            selected.append(chunk)

            used_tokens += tokens

    return selected


def format_context(
    chunks: list[dict]
) -> str:

    formatted = []

    for chunk in chunks:

        metadata = chunk.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            "unknown"
        )

        page = metadata.get(
            "page",
            1
        )

        formatted.append(
            f"[Source: {source}, Page {page}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(formatted)
