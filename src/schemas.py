from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class Feedback(BaseModel):
    name: str
    feedback_text: str


class UpdateFeedback(BaseModel):
    name: Optional[str] = None
    feedback_text: Optional[str] = None


class User(BaseModel):
    name: str
    email: str
    password: str


class DiaplayUser(User):
    id: int
    
    class Config:
        orm_mode = True


class DisplayFeedback(BaseModel):
    id: int
    name: str
    feedback_text: str
    created_at: Union[datetime, None]  
    updated_at: Union[datetime, None] 
    user: DiaplayUser
    
    class Config:
        orm_mode = True