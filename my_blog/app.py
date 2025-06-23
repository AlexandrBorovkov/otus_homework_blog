from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from my_blog.fixtures.initial_data import create_initial_data
from my_blog.posts.router import router as router_posts
from my_blog.tags.router import router as router_tags
from my_blog.templates import templates
from my_blog.users.router import router as router_users

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_initial_data()

app.include_router(router_users)
app.include_router(router_posts)
app.include_router(router_tags)
app.mount("/static", StaticFiles(directory="my_blog/static"), name="static")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
