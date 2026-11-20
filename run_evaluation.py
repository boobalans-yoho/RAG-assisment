
import json
from pathlib import Path

from app.config import settings
from app.vector_store import VectorStore
from app.retrieval import retrieve
from app.evaluation import hit_at_k

# Load golden dataset
golden_path = Path("data/golden.jsonl")
with golden_path.open("r", encoding="utf-8") as file:
    questions = [json.loads(line) for line in file if line.strip()]

# Load vector database
store = VectorStore(index_dir=settings.INDEX_DIR)
store.load()

answerable = [q for q in questions if q.get("expected_chunk_id")]
unanswerable = [q for q in questions if not q.get("expected_chunk_id")]

results = []

for item in answerable:
    retrieved = retrieve(
        query=item["question"],
        store=store,
        k=4
    )

    results.append({
        "question": item["question"],
        "hit_at_1": hit_at_k(retrieved, item["expected_chunk_id"], k=1),
        "hit_at_3": hit_at_k(retrieved, item["expected_chunk_id"], k=3),
        "hit_at_4": hit_at_k(retrieved, item["expected_chunk_id"], k=4)
    })

total = len(results)

report = {
    "total_questions": len(questions),
    "answerable_questions": len(answerable),
    "unanswerable_questions": len(unanswerable),
    "hit_at_1": round(sum(r["hit_at_1"] for r in results) / total, 4) if total else 0,
    "hit_at_3": round(sum(r["hit_at_3"] for r in results) / total, 4) if total else 0,
    "hit_at_4": round(sum(r["hit_at_4"] for r in results) / total, 4) if total else 0,
    "question_results": results
}

Path("reports").mkdir(exist_ok=True)

Path("reports/evaluation_report.json").write_text(
    json.dumps(report, indent=4),
    encoding="utf-8"
)

Path("reports/evaluation_report.txt").write_text(
    f"""RAG EVALUATION REPORT

Total Questions: {len(questions)}
Answerable Questions: {len(answerable)}
Unanswerable Questions: {len(unanswerable)}

Hit@1: {report['hit_at_1']}
Hit@3: {report['hit_at_3']}
Hit@4: {report['hit_at_4']}
""",
    encoding="utf-8"
)

print("EVALUATION COMPLETED!")
print("Total Questions:", len(questions))
print("Answerable:", len(answerable))
print("Unanswerable:", len(unanswerable))
print("Hit@1:", report["hit_at_1"])
print("Hit@3:", report["hit_at_3"])
print("Hit@4:", report["hit_at_4"])
print("Reports saved in reports/ folder")
