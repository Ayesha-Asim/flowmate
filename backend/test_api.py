from main import mock_plan, validate_plan
from datetime import date

def test_mock_plan():
    plan=validate_plan(mock_plan('Organize a community coding workshop',date(2026,11,15)))
    assert len(plan['tasks'])==5
    assert all(t['status']=='todo' for t in plan['tasks'])
    assert all(t['due_date'] for t in plan['tasks'])
