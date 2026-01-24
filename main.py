import time
from fastapi import FastAPI, APIRouter, Request, WebSocket, status
from fastapi.responses import HTMLResponse, JSONResponse
from auth import authentication
from db import models
from exceptions import StoryException
from routers import dependencies, files, posts, product, user
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from templates import templates
from client import html

app = FastAPI()
dark_theme_router = APIRouter()
app.include_router(user.router)
app.include_router(posts.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(files.router)
app.include_router(templates.router)
app.include_router(dependencies.router)

models.Base.metadata.create_all(engine)


@app.exception_handler(StoryException)
async def story_handler(req: Request, exc: StoryException):
    return JSONResponse(content={"detail": exc.name}, status_code=status.HTTP_418_IM_A_TEAPOT)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:8080"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
@app.get("/")
async def start_chat():
    return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def ws_chat(ws: WebSocket):
    await ws.accept()
    clients.append(ws) # Ws is the actual client
    while True:
        data = await ws.receive_text()
        for client in clients:
            await client.send_text(data)
            

@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers['duration'] = str(duration)
    # print("duration", duration)
    return response

app.mount(path="/files", app=StaticFiles(directory="files"), name="files")
app.mount(path="/templates/static", app=StaticFiles(directory="templates/static"), name="static")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
