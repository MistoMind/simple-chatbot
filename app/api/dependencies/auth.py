from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import settings
from crud.user import user_crud
from api.dependencies.core import get_db
from schemas.token import TokenDataSchema
from schemas.user import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/user/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenDataSchema(email=email)
    except JWTError:
        raise credentials_exception

    user = user_crud.get_by_email(db=db, email=token_data.email)

    if user is None:
        raise credentials_exception

    return user


UserDep = Annotated[UserSchema, Depends(get_current_user)]
