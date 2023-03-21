from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from ..db.user import get_user_by_username
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .token import decode_token
from ..db import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = decode_token(
        token=token, credentials_exception=credentials_exception)
    user = get_user_by_username(db=db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(user: models.User = Depends(get_current_user)):
    if user.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user
