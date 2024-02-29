from fastapi import APIRouter, HTTPException

from app.database.dependencies import dbDependency
from app.schemas.user import UserCreateSchema, UserSchema
from app.crud.user import user_crud
from app.utils import generate_password_hash

user_router = APIRouter(prefix="/user")


@user_router.post("", response_model=UserSchema)
async def register_user(user: UserCreateSchema, db: dbDependency):
    user.password = generate_password_hash(user.password)

    db_user = user_crud.get_by_email(db=db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return user_crud.create(db=db, user=user)


@user_router.get("/{id}", response_model=UserSchema)
async def get_user(id: int, db: dbDependency):
    user = user_crud.get_by_id(db=db, id=id)

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist.")

    return user


@user_router.post("/chat")
def chat(query: str):
    print(query)
    return {"response": "Reply from AI"}
