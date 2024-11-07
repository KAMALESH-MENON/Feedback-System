from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt
from src.database import get_db
from src import models, schemas

router = APIRouter(tags=["User Credentials"])


@router.post(
    "/user", response_model=schemas.DiaplayUser, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """Adds User Credentials in the database"""
    email = (
        db.query(models.UserCredential)
        .filter(models.UserCredential.email == user.email)
        .first()
    )
    if not email:
        encrpted_password = sha256_crypt.hash(user.password)
        new_user = models.UserCredential(
            name=user.name, email=user.email, password=encrpted_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already exists"
    )


@router.delete("/user/{id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Deletes User Credentials in database"""
    user = (
        db.query(models.UserCredential)
        .filter(models.UserCredential.id == user_id)
        .first()
    )
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not available"
    )
