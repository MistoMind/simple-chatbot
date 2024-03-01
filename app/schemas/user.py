from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserSchema(UserCreateSchema):
    id: int
    password: Annotated[str, Field(exclude=True)]

    class Config:
        from_attributes = True


class UserQuerySchema(BaseModel):
    question: str

    class Config:
        from_attributes = True
