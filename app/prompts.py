
def build_prompt(question: str, context: str) -> str:
    return f"""
You are an Enterprise Knowledge Assistant.

Answer the question using ONLY the context below.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is unavailable, say you do not have enough information.
4. Keep the answer clear and simple.
5. Cite the sources used in your answer.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


def build_messages(question: str, context: str) -> list:
    prompt = build_prompt(question, context)

    return [
        {
            "role": "system",
            "content": "You are a helpful Enterprise Knowledge Assistant. Use only the provided context."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
