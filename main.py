from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

feedbacks_data = {}

class Feedback(BaseModel):
    name: str
    data: str


class UpdateFeedback(BaseModel):
    name: Optional[str] = None
    data: Optional[str] = None


@app.post("/feedback/{id}")
def create_feedback(id: int, feedback: Feedback):
    if id in feedbacks_data:
        return {"error": "Feedback already exists"}

    feedbacks_data[id] = feedback
    return feedbacks_data[id]


@app.get("/feedbacks")
def get_feedbacks():
    return feedbacks_data


@app.get("/feedback/{id}")
def get_specific_feedback(id: int):
    if id in feedbacks_data:
        return feedbacks_data[id]
    return {"error": "Feedback not available"}


@app.put("/feedback/{id}")
def update_feedback(id: int, feedback: UpdateFeedback):
    if id not in feedbacks_data:
        return {"error": "Feedback ID does not exist"}

    if feedback.name is not None:
        feedbacks_data[id].name = feedback.name

    if feedback.data is not None:
        feedbacks_data[id].data = feedback.data

    return feedbacks_data[id]


@app.delete("/feedback/{id}")
def delete_feedback(id: int):
    if id not in feedbacks_data:
        return {"error": "Feedback ID does not exist"}

    del feedbacks_data[id]
    return {"message": "Deleted successfully"}
