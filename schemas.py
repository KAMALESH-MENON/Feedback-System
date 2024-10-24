from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Feedback(BaseModel):
    name: str
    feedback_text: str


class UpdateFeedback(BaseModel):
    name: Optional[str] = None
    feedback_text: Optional[str] = None

#doubt
# class DisplayFeedback(BaseModel):
#     id: int
#     name: str
#     feedback_text: str
#     created_at: datetime
#     updated_at: datetime
    
#     class config:
#         orm_mode = True