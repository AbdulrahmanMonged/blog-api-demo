from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.posts_db import (
    create_post,
    delete_post,
    get_all_posts,
    get_specfic_post,
    update_post,
)
from schemas import PostModel, PostModelDisplay, UpdatePostModel, UserModelResponse
from auth.oauth2 import get_current_user, oauth2_schema

router = APIRouter(prefix="/posts", tags=["posts"])


# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostModelDisplay)
async def create_a_post(request: PostModel, db: Session = Depends(get_db)):
    return create_post(db, request)


# READ
@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=list[PostModelDisplay]
)
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    return get_all_posts(db, user_id=user_id)


@router.get(
    "/post/{post_id}", status_code=status.HTTP_200_OK) #, response_model=PostModelDisplay

async def get_user_post(
    post_id: int, db: Session = Depends(get_db), user: UserModelResponse = Depends(get_current_user)
):
    return {"post": get_specfic_post(db, post_id), "user": user}


# UPDATE
@router.put(
    "/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostModelDisplay
)
async def update_a_post(
    post_id: int, request: UpdatePostModel, db: Session = Depends(get_db)
):
    return update_post(db, post_id, request)


# DELETE
@router.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_a_post(post_id: int, db: Session = Depends(get_db)):
    deleted_post_result = delete_post(db, post_id)
    if deleted_post_result:
        return {"message": "Post has been deleted successfully"}
