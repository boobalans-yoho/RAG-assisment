from app.context_builder import fit_context, format_context


def sample_chunks():
    return [
        {
            "id": "1",
            "text": "Employees receive 18 days of annual leave.",
            "metadata": {
                "source": "leave_policy.txt",
                "page": 1
            }
        },
        {
            "id": "2",
            "text": "Office working hours are 9 AM to 6 PM.",
            "metadata": {
                "source": "attendance_policy.txt",
                "page": 1
            }
        }
    ]


def test_fit_context_returns_list():
    result = fit_context(sample_chunks(), budget=1000)

    assert isinstance(result, list)


def test_fit_context_respects_budget():
    result = fit_context(sample_chunks(), budget=10)

    assert isinstance(result, list)


def test_format_context_returns_string():
    result = format_context(sample_chunks())

    assert isinstance(result, str)
    assert len(result) > 0