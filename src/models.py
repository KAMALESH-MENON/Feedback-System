from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Relationship
from datetime import datetime
from src.database import Base
import pytz 

INDIAN_TIMEZONE = pytz.timezone('Asia/Kolkata')

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    feedback_text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(INDIAN_TIMEZONE)) 
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(INDIAN_TIMEZONE))
    user_id = Column(Integer, ForeignKey('user_credential.id'))
    user = Relationship("UserCredential", back_populates='feedbacks')

class UserCredential(Base):
    __tablename__ = 'user_credential'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    feedbacks = Relationship("Feedback", back_populates='user')