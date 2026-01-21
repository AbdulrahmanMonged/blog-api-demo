from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base

class DbUser(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(50))

    posts: Mapped[list["Posts"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
        )


class Posts(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str]
    published: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    author: Mapped["DbUser"] = relationship(back_populates="posts")
