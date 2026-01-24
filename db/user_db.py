from sqlalchemy import select
from sqlalchemy.orm.session import Session
from db.hash import Hash
from db.models import DbUser
from schemas import BasicUserModel, UpdateUserModel, UserModel
from fastapi import HTTPException, status

def get_username_by_id(db: Session, user_id: int):
    current_username = db.scalars(select(DbUser.username).where(DbUser.id == user_id)).first()
    if current_username:
        return current_username
    raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
    
def get_user(db: Session, username: str):
    current_user = db.scalars(select(DbUser).where(DbUser.username == username)).first()
    if current_user:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id:{username} not found",
    )


def create_user(db: Session, request: UserModel):
    print(request.password)
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def verify_user(db: Session, request: BasicUserModel):
    stmnt = select(DbUser).where(DbUser.username == request.username)
    current_user = db.scalars(stmnt).first()
    if current_user:
        if Hash.verify(current_user.password, request.password):
            return current_user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with username:{request.username} not found",
    )


def get_all_users(db: Session):
    stmnt = select(DbUser)
    all_users = db.scalars(stmnt).all()
    return all_users


def update_user(db: Session, request: UpdateUserModel):
    current_user = verify_user(db, request)
    if current_user:
        current_user.username = request.username
        current_user.password = Hash.bcrypt(request.new_password)
        current_user.email = request.email
        db.commit()
        return current_user


def delete_user(db: Session, request: BasicUserModel):
    current_user = verify_user(db, request)
    if current_user:
        db.delete(current_user)
        db.commit()
        return True
    return False
