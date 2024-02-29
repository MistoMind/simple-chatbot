from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserSchema(UserCreateSchema):
    id: int

    class Config:
        from_attributes = True


class UserQuerySchema(BaseModel):
    user_id: int
    question: str

    class Config:
        from_attributes = True
