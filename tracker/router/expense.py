from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tracker import models, schemas
from tracker.database import get_db
from typing import List
from tracker.auth import oauth2
router = APIRouter(
    prefix="/expenses", 
    tags=["Expenses"]
)

@router.post("/", response_model=schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)  # 🔑 get user from token
):
    new_expense = models.Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date,
        user_id=current_user.id  # 🔑 always use token user, not request body
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db),current_user :schemas.UserResponse = Depends(oauth2.get_current_user)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.get("/", response_model=List[schemas.ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    return expenses

@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db),current_user :schemas.UserResponse = Depends(oauth2.get_current_user)):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db_expense.amount = expense.amount
    db_expense.description = expense.description
    db_expense.date = expense.date
    db_expense.user_id = expense.user_id
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db),current_user :schemas.UserResponse = Depends(oauth2.get_current_user)):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return  