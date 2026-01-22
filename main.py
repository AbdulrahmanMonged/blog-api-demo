from fastapi import FastAPI, APIRouter, Request, status
from fastapi.responses import JSONResponse
from db import models
from exceptions import StoryException
from routers import posts, product, user
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
dark_theme_router = APIRouter()
app.include_router(user.router)
app.include_router(posts.router)
app.include_router(product.router)

models.Base.metadata.create_all(engine)


@app.exception_handler(StoryException)
async def story_handler(req: Request, exc: StoryException):
    return JSONResponse(content={"detail": exc.name}, status_code=status.HTTP_418_IM_A_TEAPOT)

app.middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:8080"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
