from sqlalchemy import insert, select

from my_blog.database import async_session_maker
from my_blog.posts.exceptions import (
    RestrictionOnDeletingPostException,
    RestrictionOnUpdatingPostException,
)
from my_blog.posts.models import Post
from my_blog.tags.exceptions import (
    TagAlreadyExistsException,
    TagWasNotFoundException,
    TheTagIsUsedException,
)
from my_blog.tags.models import Tag


class TagDAO:

    model = Tag

    @classmethod
    async def add_tag(cls, **data):
        async with async_session_maker() as session:
            active_tag_query = select(cls.model).filter(
                cls.model.name == data["name"]
            )
            active_tag = await session.execute(active_tag_query)
            active_tag = active_tag.scalar_one_or_none()
            if active_tag:
                raise TagAlreadyExistsException
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_tag(cls, tag_id: int, user_id: int, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == tag_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise TagWasNotFoundException
            if row.user_id != user_id:
                raise RestrictionOnUpdatingPostException
            for key, value in data.items():
                setattr(row, key, value)
            await session.commit()

    @classmethod
    async def delete_tag(cls, tag_id: int, user_id: int):
        async with async_session_maker() as session:
            posts_query = select(Post).filter(Post.tag_id == tag_id)
            posts_result = await session.execute(posts_query)
            if posts_result.scalars().first():
                raise TheTagIsUsedException

            query = select(cls.model).filter(cls.model.id == tag_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise TagWasNotFoundException
            if row.user_id != user_id:
                raise RestrictionOnDeletingPostException
            await session.delete(row)
            await session.commit()

    @classmethod
    async def show_tag(cls, tag_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=tag_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise TagWasNotFoundException
            return row

    @classmethod
    async def get_tags(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
