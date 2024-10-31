from fastapi import FastAPI
import src.models as models
from src.database import engine
from src.routes import feedback
from src.routes import user

app = FastAPI()

app.include_router(feedback.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)