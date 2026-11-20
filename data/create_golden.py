
import json
from pathlib import Path

golden_data = [
    {
        "question": "How many days of annual leave do employees receive?",
        "expected_answer": "18 days",
        "expected_chunk_id": "39be67f6649a65634b3e5918710964d9ebcb4a0258c1b020384c5075a7a78f24",
        "expected_source": "leave_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "How many days in advance should planned leave be requested?",
        "expected_answer": "At least 5 working days",
        "expected_chunk_id": "39be67f6649a65634b3e5918710964d9ebcb4a0258c1b020384c5075a7a78f24",
        "expected_source": "leave_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "Who approves employee leave requests?",
        "expected_answer": "The manager",
        "expected_chunk_id": "39be67f6649a65634b3e5918710964d9ebcb4a0258c1b020384c5075a7a78f24",
        "expected_source": "leave_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "How many days notice must employees provide before resignation?",
        "expected_answer": "30 days",
        "expected_chunk_id": "7b6d61582bcb689b994e6cc9d325ace71b64f2555f16cb8a18b854a3e76d61a8",
        "expected_source": "resignation_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "Where should resignation letters be submitted?",
        "expected_answer": "HR department",
        "expected_chunk_id": "7b6d61582bcb689b994e6cc9d325ace71b64f2555f16cb8a18b854a3e76d61a8",
        "expected_source": "resignation_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "What are the office working hours?",
        "expected_answer": "9:00 AM to 6:00 PM",
        "expected_chunk_id": "61f65841dc14ad8d00eaf9f0b89e5e34505053aa2ccbb3e62cc469113814ec5a",
        "expected_source": "attendance_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "Which days are the regular working days?",
        "expected_answer": "Monday to Friday",
        "expected_chunk_id": "61f65841dc14ad8d00eaf9f0b89e5e34505053aa2ccbb3e62cc469113814ec5a",
        "expected_source": "attendance_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "How many working days does Finance take to process approved reimbursements?",
        "expected_answer": "10 working days",
        "expected_chunk_id": "d79eb74ed5ac00b9daaeaafddb63bc174e2c53fec7d6606ae6c6c251be7571f2",
        "expected_source": "finance_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "What is required when submitting expense claims?",
        "expected_answer": "Valid receipts",
        "expected_chunk_id": "d79eb74ed5ac00b9daaeaafddb63bc174e2c53fec7d6606ae6c6c251be7571f2",
        "expected_source": "finance_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "Who must approve business travel expenses?",
        "expected_answer": "Manager approval before travel",
        "expected_chunk_id": "d79eb74ed5ac00b9daaeaafddb63bc174e2c53fec7d6606ae6c6c251be7571f2",
        "expected_source": "finance_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "What benefits do employees receive?",
        "expected_answer": "Health insurance benefits",
        "expected_chunk_id": "48e86ba9e20f49a0abba1e1773733686e741800636d0d1b0c384c5075a7a78f24",
        "expected_source": "employee_benefits.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "Who manages employee records and recruitment?",
        "expected_answer": "Human Resources department",
        "expected_chunk_id": "cf38f9ef1624b416cd46012412d5532785e2a75513a02f643d4e3e2529d79752",
        "expected_source": "hr_policy.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "What must a strong password contain?",
        "expected_answer": "Uppercase letters, lowercase letters, numbers, and special characters",
        "expected_chunk_id": "0c92b9a4a4a9f6ee4e89ed87de0c4acc27a54ee2b5fd822ace2d1b20a3eec8b1",
        "expected_source": "it_security.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "Can employees share their passwords?",
        "expected_answer": "No, passwords must not be shared",
        "expected_chunk_id": "0c92b9a4a4a9f6ee4e89ed87de0c4acc27a54ee2b5fd822ace2d1b20a3eec8b1",
        "expected_source": "it_security.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "Who approves work from home requests?",
        "expected_answer": "Managers",
        "expected_chunk_id": "45d893f817158c5bcc49a39b44301df4175cbc7b5476ca3eab6ac68a4c1cd1d1",
        "expected_source": "work_from_home.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "How should employees report suspicious emails?",
        "expected_answer": "Report them to the IT department",
        "expected_chunk_id": "0c92b9a4a4a9f6ee4e89ed87de0c4acc27a54ee2b5fd822ace2d1b20a3eec8b1",
        "expected_source": "it_security.txt",
        "question_type": "simple_fact"
    },
    {
        "question": "What should employees do before leaving the company?",
        "expected_answer": "Complete exit formalities and return company property",
        "expected_chunk_id": "7b6d61582bcb689b994e6cc9d325ace71b64f2555f16cb8a18b854a3e76d61a8",
        "expected_source": "resignation_policy.txt",
        "question_type": "multi_chunk"
    },
    {
        "question": "What are the rules for employees working remotely?",
        "expected_answer": "Manager approval, availability during working hours, secure systems, and team meetings",
        "expected_chunk_id": "45d893f817158c5bcc49a39b44301df4175cbc7b5476ca3eab6ac68a4c1cd1d1",
        "expected_source": "work_from_home.txt",
        "question_type": "multi_chunk"
    },
    {
        "question": "What are the requirements for employee expense reimbursement?",
        "expected_answer": "Valid receipts, manager approval for business travel, and compliance with financial guidelines",
        "expected_chunk_id": "d79eb74ed5ac00b9daaeaafddb63bc174e2c53fec7d6606ae6c6c251be7571f2",
        "expected_source": "finance_policy.txt",
        "question_type": "multi_chunk"
    },
    {
        "question": "What responsibilities does the HR department have?",
        "expected_answer": "Employee records, recruitment, onboarding, employee relations, and employee development",
        "expected_chunk_id": "cf38f9ef1624b416cd46012412d5532785e2a75513a02f643d4e3e2529d79752",
        "expected_source": "hr_policy.txt",
        "question_type": "multi_chunk"
    },
    {
        "question": "What are the employee leave and sick leave procedures?",
        "expected_answer": "Submit leave requests to the manager; notify the manager for sick leave",
        "expected_chunk_id": "39be67f6649a65634b3e5918710964d9ebcb4a0258c1b020384c5075a7a78f24",
        "expected_source": "leave_policy.txt",
        "question_type": "multi_chunk"
    },
    {
        "question": "What security practices must employees follow?",
        "expected_answer": "Use strong passwords, never share passwords, avoid unauthorized devices, report suspicious emails, and use approved security software",
        "expected_chunk_id": "0c92b9a4a4a9f6ee4e89ed87de0c4acc27a54ee2b5fd822ace2d1b20a3eec8b1",
        "expected_source": "it_security.txt",
        "question_type": "multi_chunk"
    },
    {
        "question": "What is the company's policy for free international holidays?",
        "expected_answer": "I don't have information on that.",
        "expected_chunk_id": None,
        "expected_source": None,
        "question_type": "unanswerable"
    },
    {
        "question": "What is the employee bonus amount?",
        "expected_answer": "I don't have information on that.",
        "expected_chunk_id": None,
        "expected_source": None,
        "question_type": "unanswerable"
    },
    {
        "question": "How many employees work in the Chennai office?",
        "expected_answer": "I don't have information on that.",
        "expected_chunk_id": None,
        "expected_source": None,
        "question_type": "unanswerable"
    }
]

output = Path("data/golden.jsonl")
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", encoding="utf-8") as file:
    for item in golden_data:
        file.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Golden dataset created successfully!")
print("Total questions:", len(golden_data))
print("Answerable:", sum(1 for x in golden_data if x["expected_chunk_id"]))
print("Unanswerable:", sum(1 for x in golden_data if not x["expected_chunk_id"]))
print("Saved to:", output)
