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
from datetime import datetime
from datetime import timedelta
import src.config as config
from jose import jwt
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Login"],
    prefix="/login"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, config.ALGORITHM)
    return encoded_jwt


@router.post("")
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(models.UserCredential).filter(models.UserCredential.name==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found")
    if not sha256_crypt.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    access_token = generate_token(
        data={"sub": user.name}
    )
    
    return {"access_token": access_token, "token_type": "Bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={'WWW-Authenticate': "Bearer"}
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception