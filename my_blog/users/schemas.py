from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    username: str
    email: EmailStr
    password: str
