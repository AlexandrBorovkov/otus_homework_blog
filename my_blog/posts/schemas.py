from pydantic import BaseModel


class SPost(BaseModel):
    tag_id: int
    title: str
    description: str
