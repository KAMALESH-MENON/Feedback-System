from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base

INDIAN_TIMEZONE = pytz.timezone("Asia/Kolkata")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    feedback_text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(INDIAN_TIMEZONE))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(INDIAN_TIMEZONE))
    user_id = Column(Integer, ForeignKey("user_credential.id"))
    user = relationship("UserCredential", back_populates="feedbacks")


class UserCredential(Base):
    __tablename__ = "user_credential"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    feedbacks = relationship("Feedback", back_populates="user")
