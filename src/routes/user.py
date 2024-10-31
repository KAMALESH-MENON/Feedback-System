from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
import src.schemas as schemas
import src.models as models
from src.database import get_db
from passlib.hash import sha256_crypt

router = APIRouter(
    tags=['User Credentials'],
    prefix="/user"
)


@router.post("", response_model=schemas.DiaplayUser, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    email = db.query(models.UserCredential).filter(models.UserCredential.email==user.email).first()
    if not email:
        encrpted_password = sha256_crypt.hash(user.password)
        new_user = models.UserCredential(name=user.name, 
                                         email=user.email, password=encrpted_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already exists")


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserCredential).filter(models.UserCredential.id==id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not available")