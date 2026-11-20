
import csv
import json
from pathlib import Path

from .chunking import split_documents


def load_documents(folder: str) -> list[dict]:

    documents = []

    base_path = Path(folder)

    if not base_path.exists():
        return documents

    for file_path in sorted(base_path.rglob("*")):

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        try:

            if extension in [".txt", ".md"]:

                text = file_path.read_text(
                    encoding="utf-8"
                )

                documents.append({
                    "source": file_path.name,
                    "page": 1,
                    "text": text
                })

            elif extension == ".pdf":

                import fitz

                pdf = fitz.open(file_path)

                for page_number, page in enumerate(
                    pdf, start=1
                ):

                    documents.append({
                        "source": file_path.name,
                        "page": page_number,
                        "text": page.get_text()
                    })

                pdf.close()

            elif extension == ".csv":

                with open(
                    file_path,
                    encoding="utf-8-sig",
                    newline=""
                ) as file:

                    rows = list(csv.reader(file))

                text = "\n".join(
                    " | ".join(row)
                    for row in rows
                )

                documents.append({
                    "source": file_path.name,
                    "page": 1,
                    "text": text
                })

            elif extension == ".json":

                data = json.loads(
                    file_path.read_text(encoding="utf-8")
                )

                documents.append({
                    "source": file_path.name,
                    "page": 1,
                    "text": json.dumps(
                        data,
                        ensure_ascii=False
                    )
                })

        except Exception as error:

            print(
                f"Skipping {file_path.name}: {error}"
            )

    return documents


def build_chunks(
    folder: str,
    chunk_size: int = 180,
    overlap: int = 30
) -> list[dict]:

    documents = load_documents(folder)

    chunks = split_documents(
        documents,
        chunk_size,
        overlap
    )

    return chunks
