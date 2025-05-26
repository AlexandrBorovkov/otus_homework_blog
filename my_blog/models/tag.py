from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from my_blog.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship("Post", back_populates="tags")
