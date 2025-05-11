import mysql.connector
from contextlib import contextmanager
from dotenv import load_dotenv
from logger import setup_logger
import os


logger = setup_logger('db_helper')


load_dotenv(override=True)

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expense_for_date() called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * from expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses
    

def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date() called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense() called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary() called with start: {start_date} and end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) total
               FROM expenses 
               WHERE expense_date BETWEEN %s AND %s 
               GROUP BY category''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data
    

def fetch_monthly_summary():
    logger.info(f"fetch_monthly_summary() called.")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
            SELECT year(expense_date) year, month(expense_date) month, sum(amount) total 
            FROM expenses 
            GROUP BY year(expense_date), month(expense_date)'''
        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-08-01")
    print(expenses)
    insert_expense("2024-08-01", 50, "Food", "Puffs")
    delete_expense_for_date("2024-08-01")
    summary = fetch_expense_summary("2024-08-03", "2024-08-04")
    print(summary)
    data = fetch_monthly_summary()
    print(data)