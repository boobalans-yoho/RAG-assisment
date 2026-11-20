
from openai import OpenAI

from .config import get_settings
from .prompts import build_messages


ABSTAIN = "I don't have information on that."


def generate_answer(
    question: str,
    chunks: list[dict]
) -> str:

    settings = get_settings()

    if not settings.OPENROUTER_API_KEY:

        raise RuntimeError(
            "OPENROUTER_API_KEY is missing in .env"
        )

    context_parts = []

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

        context_parts.append(
            f"[Source: {source}, Page {page}]\n"
            f"{chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    messages = build_messages(
        question,
        context
    )

    client = OpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL
    )

    response = client.chat.completions.create(
        model=settings.OPENROUTER_MODEL,
        messages=messages,
        temperature=0
    )

    answer = response.choices[0].message.content

    if not answer:
        return ABSTAIN

    return answer.strip()
