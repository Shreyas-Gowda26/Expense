from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tracker import models, schemas
from tracker.database import get_db
from typing import List
from tracker.auth import oauth2 
router = APIRouter(
    prefix="/budget",
    tags=["Budget"]
)

@router.post("/", response_model=schemas.BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    new_budget = models.Budget(
        total_amount=budget.total_amount,
        start_date=budget.start_date,
        end_date=budget.end_date,
        user_id=budget.user_id
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

@router.get("/{budget_id}", response_model=schemas.BudgetResponse)
def get_budget(budget_id: int, db: Session = Depends(get_db),current_user :schemas.UserResponse = Depends(oauth2.get_current_user)): 
    budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.get("/", response_model=List[schemas.BudgetResponse])
def get_budgets(db: Session = Depends(get_db)):
    budgets = db.query(models.Budget).all()
    return budgets

@router.put("/{budget_id}", response_model=schemas.BudgetResponse)
def update_budget(budget_id: int, budget: schemas.BudgetCreate, db: Session = Depends(get_db),current_user :schemas.UserResponse = Depends(oauth2.get_current_user)):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    db_budget.total_amount = budget.total_amount
    db_budget.start_date = budget.start_date
    db_budget.end_date = budget.end_date
    db_budget.user_id = budget.user_id
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, db: Session = Depends(get_db),current_user :schemas.UserResponse = Depends(oauth2.get_current_user)):       
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(db_budget)
    db.commit()
    return