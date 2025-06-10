from sqlalchemy import insert, select

from my_blog.database import async_session_maker
from my_blog.posts.exceptions import (
    PostAlreadyExistsException,
    PostWasNotFoundException,
)
from my_blog.posts.models import Post


class PostDAO:

    model = Post

    @classmethod
    async def add_post(cls, **data):
        async with async_session_maker() as session:
            active_post_query = select(cls.model).filter(
                cls.model.title == data["title"]
            )
            active_post = await session.execute(active_post_query)
            active_post = active_post.scalar_one_or_none()
            if active_post:
                raise PostAlreadyExistsException
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_post(cls, post_id: int, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == post_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise PostWasNotFoundException
            for key, value in data.items():
                setattr(row, key, value)
            await session.commit()

    @classmethod
    async def delete_post(cls, post_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == post_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise PostWasNotFoundException
            await session.delete(row)
            await session.commit()

    @classmethod
    async def show_post(cls, post_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=post_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise PostWasNotFoundException
            return row

    @classmethod
    async def get_posts(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
