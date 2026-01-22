from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from db.models import Posts
from db.user_db import get_user
from exceptions import StoryException
from schemas import PostModel, UpdatePostModel


def create_post(db: Session, request: PostModel):
    current_user = get_user(db, request.user_id)
    if current_user:
        if request.content.startswith("once upon time"):
            raise StoryException("You can't start a story.")
        
        new_post = Posts(
            title=request.title, content=request.content, user_id=request.user_id
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    raise HTTPException(
        detail=f"User with id:{request.user_id} Not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )


def get_all_posts(db: Session, user_id: int):
    current_user = get_user(db, user_id)
    if current_user:
        return current_user.posts


def get_specfic_post(db: Session, post_id: int):
    post = db.scalars(select(Posts).where(Posts.id == post_id)).first()
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id:{post_id} not found",
    )


def update_post(db: Session, post_id: int, request: UpdatePostModel):
    post = get_specfic_post(db, post_id)
    if post:
        post.title = request.title
        post.content = request.content
        post.published = request.published
        db.commit()
        return post


def delete_post(db: Session, post_id: int):
    post = get_specfic_post(db, post_id)
    if post:
        db.delete(post)
        db.commit()
        return True
    return False
