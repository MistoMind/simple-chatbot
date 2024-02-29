from fastapi import APIRouter, HTTPException, status
from openai import RateLimitError

from api.dependencies.chatbot import ChainDep, HistoryDep
from api.dependencies.core import dbDependency
from schemas.user import UserCreateSchema, UserSchema, UserQuerySchema
from crud.user import user_crud
from utils import generate_password_hash

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
async def chat_with_ai(
    query: UserQuerySchema, chain: ChainDep, chat_history: HistoryDep
):
    chat_history.add_user_message(query.question)

    try:
        ai_response = chain.invoke({"messages": chat_history.messages})
    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rate limit exceeded.",
        )

    chat_history.add_ai_message(ai_response.content)

    return {"response": ai_response.content}
