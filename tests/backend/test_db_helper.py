from backend import db_helper
import sys

print(sys.path)

def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")

    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'] == "Shopping"
    assert expenses[0]['notes'] == "Bought potatoes"


def test_delete_expenses_for_date():
    db_helper.delete_expense_for_date("2024-08-02")
    expenses = db_helper.fetch_expenses_for_date("2024-08-02")

    assert len(expenses) == 0


def test_insert_expenses():
    db_helper.insert_expense("2024-08-02", 50, "Food", "2 Puffs")
    expenses = db_helper.fetch_expenses_for_date("2024-08-02")
    print("Fetched expenses:", expenses)

    assert len(expenses) > 0
    assert any(str(e['expense_date']) == "2024-08-02" for e in expenses)
    assert any(e['amount'] == 50 for e in expenses)
    assert any(e['category'] == "Food" for e in expenses)
    assert any(e['notes'] == "2 Puffs" for e in expenses)


def test_fetch_expense_summary():
    expected = [
        {'category': 'Food', 'total_amount': 185.0},
        {'category': 'Entertainment', 'total_amount': 20.0},
        {'category': 'Shopping', 'total_amount': 320.0},
        {'category': 'Other', 'total_amount': 25.0},
    ]

    results = db_helper.fetch_expense_summary("2024-08-03", "2024-08-04")

    assert sorted(results, key=lambda x: x['category']) == sorted(expected, key=lambda x: x['category'])

