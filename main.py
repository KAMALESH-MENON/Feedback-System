from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

feedbacks_data = {
    1 : {
        "name" : "Kamalesh",
        "data" : "GRADUATE TRIANEE"
    }
}

class Feedback(BaseModel):
    name : str
    data : str

class updateFeedback(BaseModel):
    name : Optional[str] = None
    data : Optional[str] = None

@app.get("/")
def Feedback():
    return {"hi" : "testing"}

@app.post("/post/feedback/id")
def createFeedback(id : int, feedback : Feedback):
    if id in feedbacks_data:
        return {"Error" : "Already Exist"}
    feedbacks_data[id] = feedback
    return feedbacks_data[id]

@app.get("/get/feedback")
def getFeedback():
    return feedbacks_data

@app.get("/get/feedback/{id}")
def getSpecificFeedback(id : int):
    if id in feedbacks_data:
        return feedbacks_data[id]
    return {"Error": "Data not available"}

@app.put("/put/feedback/{id}")
def updateFeedback(id : int, feedback : updateFeedback):
    if id not in feedbacks_data:
        return {"Error" : "id does not exist"}

    if feedback.name != None:
        feedbacks_data[id].name = feedback.name
    if feedback.data != None:
        feedbacks_data[id].data = feedback.data

    return feedbacks_data[id]

@app.delete("/delete/feedback/{id}")
def deleteFeedback(id : int):
    if id not in feedbacks_data:
        return {"Error" : "id does not exist"}
    
    del feedbacks_data[id]
    return {"Message" : "Deleted Successfully"}