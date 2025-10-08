from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class ExpenseCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    date: date  # ISO format date string
    category: Optional[str] = None
    user_id: int

class ExpenseResponse(ExpenseCreate):
    id: int

    class Config:
        orm_mode = True

class BudgetCreate(BaseModel):
    total_amount: float
    start_date: str  # ISO format date string
    end_date: str  # ISO format date string
    user_id: int

class BudgetResponse(BudgetCreate):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

