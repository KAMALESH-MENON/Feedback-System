from fastapi import FastAPI
import src.models as models
from src.database import engine
from src.routes import feedback
from src.routes import user
from src.routes import login

app = FastAPI()

app.include_router(feedback.router)
app.include_router(user.router)
app.include_router(login.router)

models.Base.metadata.create_all(engine)
