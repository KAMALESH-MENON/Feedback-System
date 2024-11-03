from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.routes.login import get_current_user
from typing import List
from src import schemas
from src import models

router = APIRouter(
    tags=['Feedback'],
    prefix="/feedback"
)


@router.get("", response_model=List[schemas.DisplayFeedback])
def get_feedbacks(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Retrieves all the feedback"""
    feedbacks = db.query(models.Feedback).all()
    if feedbacks:
        return feedbacks
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empty Database")


@router.post("", response_model=schemas.DisplayFeedback, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: schemas.Feedback, db: Session = Depends(get_db),
                    current_user: schemas.User = Depends(get_current_user)):
    """Creates new feedback if it does not already exist"""
    existing_user = db.query(models.UserCredential).filter(
                            models.UserCredential.id==feedback.id).first()
    if existing_user:
        new_feedback = models.Feedback(name=feedback.name,
                                       feedback_text=feedback.feedback_text,
                                       user_id=feedback.id)
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        return new_feedback
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                        detail="Given User_id does not exist. Add the User first.")


@router.get("/{id}", response_model=schemas.DisplayFeedback)
def get_specific_feedback(user_id: int, db: Session = Depends(get_db),
                          current_user: schemas.User = Depends(get_current_user)):
    """Retrieves feedback of the given id"""
    feedback = db.query(models.Feedback).filter(models.Feedback.id == user_id).first()
    if feedback:
        return feedback
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not available")


@router.put("/{id}", response_model=schemas.DisplayFeedback)
def update_feedback(user_id: int, update_feedback: schemas.UpdateFeedback,
                    db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Updates the feedback details such as name and feedback_text in database"""
    feedback = db.query(models.Feedback).filter(models.Feedback.id == user_id).first()
    if feedback:
        if feedback.name is not None:
            feedback.name = update_feedback.name
        if feedback.feedback_text is not None:
            feedback.feedback_text = update_feedback.feedback_text
        db.commit()
        db.refresh(feedback)
        return feedback
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not available")


@router.delete("/{id}")
def delete_feedback(user_id: int, db: Session = Depends(get_db),
                    current_user: schemas.User = Depends(get_current_user)):
    """Deletes the feedback from the database"""
    feedback = db.query(models.Feedback).filter(models.Feedback.id == user_id).first()
    if feedback:
        db.delete(feedback)
        db.commit()
        return {"message": "feedback deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not available")
