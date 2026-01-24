from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.user_db import verify_user
from .oauth2 import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token")
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    current_user = verify_user(db, request)
    if current_user:
        decoded_token = create_access_token({'sub': current_user.username})
        return {
            "access_token": decoded_token,
            "token_type": "Bearer"
        } 