from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

feedbacks_data = {}


class Feedback(BaseModel):
    name: str
    data: str


class UpdateFeedback(BaseModel):
    name: Optional[str] = None
    data: Optional[str] = None


def load_data():
    try:
        with open("feedbackData.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("feedbackData.json", 'a') as f:
            f.write("{}")
        return json.load(f)


def save_data(data):
    with open("feedbackData.json", "w") as f:
        json.dump(data, f)


@app.post("/feedback")
def create_feedback(feedback: Feedback):
    feedbacks_data = load_data()
    if feedbacks_data:
        id = max(map(int, feedbacks_data.keys())) + 1
    else:
        id = 1

    feedbacks_data[id] = feedback.dict()
    save_data(feedbacks_data)
    return feedbacks_data[id]


@app.get("/feedbacks")
def get_feedbacks():
    feedbacks_data = load_data()
    return feedbacks_data


@app.get("/feedback/{id}")
def get_specific_feedback(id: int):
    feedbacks_data = load_data()
    if str(id) in feedbacks_data:
        return feedbacks_data[str(id)]

    return {"error": "Feedback not available"}


@app.put("/feedback/{id}")
def update_feedback(id: int, feedback: UpdateFeedback):
    feedbacks_data = load_data()
    if str(id)  in feedbacks_data:
        if feedback.name is not None:
            feedbacks_data[str(id)]["name"] = feedback.name

        if feedback.data is not None:
            feedbacks_data[str(id)]["data"] = feedback.data

        save_data(feedbacks_data)
        return feedbacks_data[str(id)]
        
    return {"error": "Feedback ID does not exist"}


@app.delete("/feedback/{id}")
def delete_feedback(id: int):
    feedbacks_data = load_data()
    if str(id) in feedbacks_data:
        del feedbacks_data[str(id)]
        save_data(feedbacks_data)
        return {"message": "Deleted successfully"}
    
    return {"error": "Feedback ID does not exist"}
