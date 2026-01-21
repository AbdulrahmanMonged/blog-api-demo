from fastapi import FastAPI, APIRouter
from db import models
from routers import posts, user
import fastapi_swagger_dark as fsd
from db.database import engine

app = FastAPI()
dark_theme_router = APIRouter()
app.include_router(user.router)
app.include_router(posts.router)

models.Base.metadata.create_all(engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)