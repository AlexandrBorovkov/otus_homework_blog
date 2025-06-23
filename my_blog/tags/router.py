from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from my_blog.tags.dao import TagDAO
from my_blog.tags.schemas import STag
from my_blog.templates import templates
from my_blog.users.dependencies import get_current_user
from my_blog.users.models import User

router = APIRouter(prefix="/tags", tags=["Теги"])


@router.get("/tag_processing")
async def show_tag_processing_form(
    request: Request,
    user: User = Depends(get_current_user)
):
    tags = await TagDAO.get_tags()
    return templates.TemplateResponse(
        "tags/tag_processing.html",
        {"request": request, "tags": tags, "current_user": user}
    )

@router.post("/add_tag")
async def add_tag(
    name: str = Form(...),
    user: User = Depends(get_current_user)
):
    await TagDAO.add_tag(
        user_id=user.id,
        name=name,
    )
    return RedirectResponse(url="/tags/tag_processing", status_code=303)

@router.get("/update_tag/{tag_id}")
async def edit_tag(
    tag_id: int,
    request: Request,
    user: User = Depends(get_current_user)
):
    tag = await TagDAO.show_tag(tag_id)
    return templates.TemplateResponse(
        "tags/update_tag.html",
        {"request": request, "tag": tag}
    )

@router.post("/update_tag/{tag_id}")
async def update_tag(
    tag_id: int,
    name: str = Form(...),
    user: User = Depends(get_current_user)
):
    await TagDAO.update_tag(
        tag_id,
        user_id=user.id,
        name=name
    )
    return RedirectResponse(url="/tags/tag_processing", status_code=303)

@router.post("/delete_tag")
async def delete_tag(
    tag_id: int = Form(...),
    user: User = Depends(get_current_user)
):
    await TagDAO.delete_tag(tag_id, user.id)
    return RedirectResponse(url="/tags/tag_processing", status_code=303)
