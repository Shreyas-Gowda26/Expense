from fastapi import APIRouter
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from tracker import database, models
from tracker.auth import auth
from tracker.router import user, expense,budget
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
app.mount("/static", StaticFiles(directory="tracker/static"), name="static")


app.include_router(user.router)
app.include_router(budget.router)
app.include_router(expense.router)
app.include_router(auth.router)