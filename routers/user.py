
from anyio import Path
from fastapi import APIRouter, Depends, status
from httpx import request
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.user_db import create_user, delete_user, get_all_users, update_user, verify_user
from schemas import BasicUserModel, UpdateUserModel, UserModel, UserModelResponse

router = APIRouter(prefix="/user", tags=['user'])

# Create User
@router.post("/", response_model=UserModelResponse, status_code=status.HTTP_201_CREATED)
async def user_creation(request: UserModel, db: Session = Depends(get_db)):
    return create_user(db, request)


# Get User
@router.post("/login", response_model=UserModelResponse, status_code=status.HTTP_200_OK)
async def get_user(request: BasicUserModel, db: Session = Depends(get_db)):
    return verify_user(db, request)
    
# Get All users
@router.get('/', status_code=status.HTTP_200_OK, response_model=list[UserModelResponse])
async def fetch_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


# Update User
@router.put("/", response_model=UserModelResponse, status_code=status.HTTP_200_OK)
async def update_current_user(request: UpdateUserModel, db: Session = Depends(get_db)):
    return update_user(db, request)

@router.delete("/")
async def delete_current_user(request: BasicUserModel, db: Session = Depends(get_db)):
    delete_user(db, request)
    return {"status": "User deleted successfully"}
    
# Delete User