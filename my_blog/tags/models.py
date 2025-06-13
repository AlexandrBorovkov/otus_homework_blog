from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from my_blog.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, unique=True, nullable=False)

    posts = relationship("Post", back_populates="tags", passive_deletes='all')
    users = relationship("User", back_populates="tags")
