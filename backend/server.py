from fastapi import FastAPI, HTTPException
from datetime import date
from backend import db_helper
from typing import List
from pydantic import BaseModel

app = FastAPI()
class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expense(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)

    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to receive expense from the data base.")
    
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses:List[Expense]):
    db_helper.delete_expense_for_date(expense_date)

    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    
    return {"message": "Expense updated successfully"}


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)

    if data is None:
        raise HTTPException(status_code=500, detail="Failed to receive expense summary from the data base.")
    
    total = sum([row['total'] for row in data])

    breakdown = {}

    for row in data:
        percentage = round(row['total']/total*100,1) if total !=0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }

    return breakdown


@app.post("/monthly/")
def monthly_summary():
    data = db_helper.fetch_monthly_summary()

    if data is None:
        raise HTTPException(status_code=500, detail="Failed to receive summary from the data base.")
    
    summary = {'year': [],
               'month': [],
               'total': []
               }

    for row in data:
        summary['year'].append(row['year'])
        summary['month'].append(row['month'])
        summary['total'].append(row['total'])

    return summary