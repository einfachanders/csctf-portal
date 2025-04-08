from typing import Any
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.types import Text

class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON
    }

class User(Base):
    """Class representing a User in the database
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    created: Mapped[datetime] = mapped_column(default=func.now()) # pylint: disable=not-callable

class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    flag: Mapped[str]
