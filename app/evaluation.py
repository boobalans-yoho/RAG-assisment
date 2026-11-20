
import json

from pathlib import Path


def load_golden(
    path: str = "data/golden.jsonl"
) -> list[dict]:

    file_path = Path(path)

    if not file_path.exists():
        return []

    questions = []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            if line.strip():

                questions.append(
                    json.loads(line)
                )

    return questions


def hit_at_k(
    results: list[dict],
    expected_chunk_id: str | set[str] | list[str],
    k: int = 3
) -> float:

    if isinstance(expected_chunk_id, str):
        relevant_ids = {expected_chunk_id}
    else:
        relevant_ids = set(expected_chunk_id)

    for result in results[:k]:
        if result.get("id") in relevant_ids:
            return 1.0

    return 0.0


def calculate_hit_rate(
    results: list[list[dict]],
    expected_ids: list[str],
    k: int = 3
) -> float:

    if not expected_ids:
        return 0.0

    hits = 0

    for retrieved, expected in zip(
        results,
        expected_ids
    ):

        hits += hit_at_k(
            retrieved,
            expected,
            k
        )

    return hits / len(expected_ids)


def manual_faithfulness(
    claims: list[str],
    supported_claims: list[bool]
) -> float:

    if not claims:
        return 0.0

    if len(claims) != len(supported_claims):

        raise ValueError(
            "Claims and support labels must have equal length"
        )

    supported = sum(supported_claims)

    return supported / len(claims)


def save_jsonl(
    rows: list[dict],
    path: str
):

    file_path = Path(path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        for row in rows:

            file.write(
                json.dumps(
                    row,
                    ensure_ascii=False
                ) + "\n"
            )
