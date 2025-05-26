from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from my_blog.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

session_maker = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
