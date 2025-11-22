"""Example router for users demonstrating modular structure."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    # Placeholder implementation until real user model exists
    return {"message": "List of users"}


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return {"message": f"User {user_id}"}


@router.post("/")
def create_user(db: Session = Depends(get_db)):
    return {"message": "User created"}
