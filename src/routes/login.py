from fastapi import APIRouter
from fastapi import APIRouter
from fastapi import Depends
from src.database import get_db
from fastapi import status
from sqlalchemy.orm import Session
from fastapi import HTTPException
import src.schemas as schemas
import src.models as models
from passlib.hash import sha256_crypt

router = APIRouter(
    prefix="/login"
)

@router.post("")
def login(request: schemas.Login, db: Session=Depends(get_db)):
    user = db.query(models.UserCredential).filter(models.UserCredential.name==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found")
    if not sha256_crypt.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    
    return request