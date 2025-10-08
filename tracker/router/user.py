from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from tracker import models,schemas
from tracker.database import get_db
from typing import List
from tracker.auth import oauth2
from tracker.hashing import hash_password
router = APIRouter(
    prefix="/users",
    tags=["Users"]  
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password) # In a real app, hash the password!
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db),current_user :schemas.UserResponse = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users    

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db),current_user :schemas.UserResponse = Depends(oauth2.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return  