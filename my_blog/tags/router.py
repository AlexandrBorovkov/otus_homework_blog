from fastapi import APIRouter, Depends

from my_blog.tags.dao import TagDAO
from my_blog.tags.schemas import STag
from my_blog.users.dependencies import get_current_user
from my_blog.users.models import User

router = APIRouter(prefix="/tags", tags=["Теги"])


@router.post("/add_tag")
async def add_tag(
    tag: STag,
    user: User = Depends(get_current_user)
):
    await TagDAO.add_tag(
        user_id=user.id,
        name=tag.name,
    )

@router.patch("/update_tag")
async def update_tag(
    tag_id: int,
    tag: STag,
    user: User = Depends(get_current_user)
):
    await TagDAO.update_tag(
        tag_id,
        user_id=user.id,
        name=tag.name
    )

@router.delete("/delete_tag")
async def delete_tag(
    tag_id: int,
    user: User = Depends(get_current_user)
):
    await TagDAO.delete_tag(tag_id, user.id)

@router.get("/show_tag")
async def show_tag(
    tag_id: int,
    user: User = Depends(get_current_user)
):
    result = await TagDAO.show_tag(tag_id)
    return result

@router.get("/all_tags")
async def get_tags(user: User = Depends(get_current_user)):
    result = await TagDAO.get_tags()
    return result
