from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse

from my_blog.posts.dao import PostDAO
from my_blog.posts.schemas import SPost
from my_blog.tags.dao import TagDAO
from my_blog.templates import templates
from my_blog.users.dependencies import get_current_user
from my_blog.users.models import User

router = APIRouter(prefix="/posts", tags=["Посты"])


@router.get("/add_post")
async def show_create_post_form(
    request: Request,
    user: User = Depends(get_current_user)
):
    tags = await TagDAO.get_tags()
    return templates.TemplateResponse("posts/create_post.html", {"request": request, "tags": tags})

@router.post("/add_post")
async def add_post(
    tag_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    user: User = Depends(get_current_user)
):
    print(tag_id, title, description, user.id)
    await PostDAO.add_post(
        user_id=user.id,
        tag_id=tag_id,
        title=title,
        description=description.replace("\n", "<br>")
    )
    return RedirectResponse(url="/posts/all_posts", status_code=303)

@router.get("/update_post/{post_id}")
async def edit_post(
    post_id: int,
    request: Request,
    user: User = Depends(get_current_user)
):
    post = await PostDAO.show_post(post_id)
    tags = await TagDAO.get_tags()
    return templates.TemplateResponse(
        "posts/update_post.html",
        {"request": request, "post": post, "tags": tags}
    )

@router.post("/update_post/{post_id}")
async def update_post(
    post_id: int,
    tag_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    user: User = Depends(get_current_user)
):
    await PostDAO.update_post(
        post_id=post_id,
        user_id=user.id,
        tag_id=tag_id,
        title=title,
        description=description.replace("\n", "<br>")
    )
    return RedirectResponse(url="/posts/all_posts", status_code=303)

@router.post("/delete_post")
async def delete_post(
    post_id: int = Form(...),
    user: User = Depends(get_current_user)
):
    await PostDAO.delete_post(post_id, user.id)
    return RedirectResponse(url="/posts/all_posts", status_code=303)

@router.get("/show_post/{post_id}")
async def show_post(
    post_id: int,
    request: Request,
    user: User = Depends(get_current_user)
):
    result = await PostDAO.show_post(post_id)
    return templates.TemplateResponse("posts/show_program.html", {"request": request, "post": result, "current_user": user})

@router.get("/all_posts")
async def get_posts(request: Request):
    result = await PostDAO.get_posts()
    return templates.TemplateResponse("posts/training_programs.html", {"request": request, "posts": result})

@router.get("/posts_by_tags/{tag_id}")
async def get_posts_by_tags(
    tag_id: int,
    request: Request,
    user: User = Depends(get_current_user)
):
    result = await PostDAO.get_posts_by_tags(tag_id)
    return templates.TemplateResponse("posts/training_programs.html", {"request": request, "posts": result})
