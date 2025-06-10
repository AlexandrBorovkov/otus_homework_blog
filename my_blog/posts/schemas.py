from pydantic import BaseModel


class SPost(BaseModel):
    title: str
    description: str
