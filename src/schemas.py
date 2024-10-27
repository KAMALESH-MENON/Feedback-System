from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class Feedback(BaseModel):
    name: str
    feedback_text: str


class UpdateFeedback(BaseModel):
    name: Optional[str] = None
    feedback_text: Optional[str] = None


class DisplayFeedback(BaseModel):
    id: int
    name: str
    feedback_text: str
    created_at: Union[datetime, None]  
    updated_at: Union[datetime, None] 
    
    class Config:
        orm_mode = True