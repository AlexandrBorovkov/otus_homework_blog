from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from my_blog.posts.router import router as router_posts
from my_blog.tags.router import router as router_tags
from my_blog.users.router import router as router_users

app = FastAPI()
app.include_router(router_users)
app.include_router(router_posts)
app.include_router(router_tags)
templates = Jinja2Templates(directory="my_blog/templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
