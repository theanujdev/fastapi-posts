from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..db.user import get_user_by_username
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..auth.hash import Hash
from ..auth.token import create_access_token

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = get_user_by_username(db=db, username=form_data.username)
    if not user:
        raise credentials_exception
    if not Hash.verify_password(form_data.password, user.password):  # type: ignore
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
