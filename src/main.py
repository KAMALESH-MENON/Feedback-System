from fastapi import FastAPI
from fastapi import Depends
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
import src.schemas as schemas
import src.models as models
from src.database import engine
from src.database import SessionLocal
from typing import List
from hashlib import sha256

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/feedback", response_model=List[schemas.DisplayFeedback])
def get_feedbacks(db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).all()
    if feedbacks:
        return feedbacks
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empty Database")


@app.post("/feedback", response_model=schemas.DisplayFeedback, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: schemas.Feedback, db: Session = Depends(get_db)):
    new_feedback = models.Feedback(name=feedback.name, feedback_text=feedback.feedback_text)
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


@app.get("/feedback/{id}", response_model=schemas.DisplayFeedback)
def get_specific_feedback(id: int, response: Response, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == id).first()
    if feedback:
        return feedback 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not available")


@app.put("/feedback/{id}", response_model=schemas.DisplayFeedback)
def update_feedback(id: int, response: Response, feedback: schemas.UpdateFeedback, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == id).first()
    if feedback:
        if feedback.name is not None:
            feedback.name = feedback.name
        if feedback.feedback_text is not None:
            feedback.feedback_text = feedback.feedback_text
        db.commit()
        db.refresh(feedback)
        return feedback
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not available")


@app.delete("/feedback/{id}")
def delete_feedback(id: int, response: Response, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == id).first()
    if feedback:
        db.delete(feedback)
        db.commit()
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not available")


@app.post("/user", response_model=schemas.DiaplayUser, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    encrpted_password = sha256(user.password.encode('utf-8')).hexdigest()
    
    new_user = models.UserCredential(name=user.name, email=user.email, password=encrpted_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user