from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from datetime import datetime


class Feedback(BaseModel):
    name: str
    feedback_text: str
    id: int


class UpdateFeedback(BaseModel):
    name: Optional[str] = None
    feedback_text: Optional[str] = None


class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class DiaplayUser(User):
    id: int
    
    class Config:
        from_attributes = True


class DisplayFeedback(BaseModel):
    id: int
    name: str
    feedback_text: str
    created_at: Union[datetime, None]  
    updated_at: Union[datetime, None] 
    user: DiaplayUser

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None