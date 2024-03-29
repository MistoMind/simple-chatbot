from fastapi import Depends
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Annotated

from config import settings


chat = ChatOpenAI(
    model="gpt-3.5-turbo-1106", temperature=0.2, api_key=settings.openai_api_key
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | chat


def get_chain():
    return chain


ChainDep = Annotated[ChatOpenAI | ChatPromptTemplate, Depends(get_chain)]
