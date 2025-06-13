from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from my_blog.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tag_id = Column(
        Integer,
        ForeignKey("tags.id", ondelete="RESTRICT"),
        nullable=False
    )
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="posts")
    tags = relationship("Tag", back_populates="posts")
