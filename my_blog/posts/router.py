from fastapi import APIRouter, Depends, Request

from my_blog.posts.dao import PostDAO
from my_blog.posts.schemas import SPost
from my_blog.templates import templates
from my_blog.users.dependencies import get_current_user
from my_blog.users.models import User

router = APIRouter(prefix="/posts", tags=["Посты"])


@router.post("/add_post")
async def add_post(
    post: SPost,
    user: User = Depends(get_current_user)
):
    await PostDAO.add_post(
        user_id=user.id,
        tag_id=post.tag_id,
        title=post.title,
        description=post.description.replace("\n", "<br>")
    )

@router.patch("/update_post")
async def update_post(
    post_id: int,
    post: SPost,
    user: User = Depends(get_current_user)
):
    await PostDAO.update_post(
        post_id,
        user_id=user.id,
        title=post.title,
        description=post.description.replace("\n", "<br>")
    )

@router.delete("/delete_post")
async def delete_post(
    post_id: int,
    user: User = Depends(get_current_user)
):
    await PostDAO.delete_post(post_id, user.id)

@router.get("/show_post/{post_id}")
async def show_post(
    post_id: int,
    request: Request,
    user: User = Depends(get_current_user)
):
    result = await PostDAO.show_post(post_id)
    return templates.TemplateResponse("show_program.html", {"request": request, "post": result})

@router.get("/all_posts")
async def get_posts(request: Request):
    result = await PostDAO.get_posts()
    return templates.TemplateResponse("training_programs.html", {"request": request, "posts": result})

@router.get("/posts_by_tags/{tag_id}")
async def get_posts_by_tags(
    tag_id: int,
    request: Request,
    user: User = Depends(get_current_user)
):
    result = await PostDAO.get_posts_by_tags(tag_id)
    return templates.TemplateResponse("training_programs.html", {"request": request, "posts": result})
