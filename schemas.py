from xmlrpc.client import boolean
from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str
    email: str


class BasicUserModel(BaseModel):
    username: str
    password: str


class UserModelResponse(BaseModel):
    username: str
    email: str
    posts: list["PostModelDisplay"]


class UpdateUserModel(BaseModel):
    username: str
    password: str
    new_password: str
    email: str


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    user_id: int


class SimpleUserModel(BaseModel):
    username: str


class PostModelDisplay(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    author: SimpleUserModel


class UpdatePostModel(BaseModel):
    title: str
    content: str
    published: boolean


class ProductBase(BaseModel):
    title: str
    description: str
    price: str