from fastapi import APIRouter, HTTPException, status
from langchain.memory import PostgresChatMessageHistory
from openai import RateLimitError

from config import settings
from api.dependencies.auth import UserDep
from api.dependencies.chatbot import ChainDep
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


@user_router.get("", response_model=UserSchema)
async def get_user(user: UserDep, db: dbDependency):
    user = user_crud.get_by_id(db=db, id=user.id)

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist.")

    return user


@user_router.post("/chat")
async def chat_with_ai(query: UserQuerySchema, user: UserDep, chain: ChainDep):
    chat_history = PostgresChatMessageHistory(
        session_id=str(user.id),
        connection_string=settings.database_url,
        table_name=settings.chat_history_table,
    )

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
