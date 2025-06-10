from fastapi import APIRouter, Depends

from my_blog.posts.dao import PostDAO
from my_blog.posts.schemas import SPost
from my_blog.users.dependencies import get_current_user
from my_blog.users.models import User

router = APIRouter(prefix="/posts", tags=["Посты"])


@router.post("/add_post")
async def add_post(
    post: SPost,
    user: User = Depends(get_current_user)
):
    await PostDAO.add_post(
        user_id=user.user_id,
        tag_id=post.tag_id,
        title=post.title,
        description=post.description
    )

@router.patch("/update_post")
async def update_post(
    post_id: int,
    post: SPost,
    user: User = Depends(get_current_user)
):
    await PostDAO.update_post(
        post_id,
        title=post.title,
        description=post.description
    )

@router.delete("/delete_post")
async def delete_post(
    post_id: int,
    user: User = Depends(get_current_user)
):
    await PostDAO.delete_post(post_id)

@router.get("/show_post")
async def show_post(
    post_id: int,
    user: User = Depends(get_current_user)
):
    result = await PostDAO.show_post(post_id)
    return result

@router.get("/all_posts")
async def get_posts(user: User = Depends(get_current_user)):
    result = await PostDAO.get_posts()
    return result
