from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas
import models
from database import engine, SessionLocal
from typing import List
from pytz import timezone

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/feedbacks", response_model=List[schemas.DisplayFeedback])
def get_feedbacks(db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).all()
    return feedbacks


@app.post("/feedback", response_model=schemas.DisplayFeedback   )
def create_feedback(feedback: schemas.Feedback, db: Session = Depends(get_db)):
    new_feedback = models.Feedback(name=feedback.name, feedback_text=feedback.feedback_text)
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


@app.get("/feedback/{id}", response_model=schemas.DisplayFeedback)
def get_specific_feedback(id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == id).first()
    if feedback:
        return feedback
    return {"error": "Feedback not available"}


@app.put("/feedback/{id}", response_model=schemas.DisplayFeedback)
def update_feedback(id: int, feedback: schemas.UpdateFeedback, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == id).first()
    if feedback:
        if feedback.name is not None:
            feedback.name = feedback.name
        if feedback.feedback_text is not None:
            feedback.feedback_text = feedback.feedback_text
        db.commit()
        db.refresh(feedback)
        return feedback
    return {"error": "Feedback ID does not exist"}


@app.delete("/feedback/{id}")
def delete_feedback(id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == id).first()
    if feedback:
        db.delete(feedback)
        db.commit()
        return {"message": "Deleted successfully"}
    return {"error": "Feedback ID does not exist"}