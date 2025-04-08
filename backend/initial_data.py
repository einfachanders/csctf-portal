from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.core.config import settings
import app.crud as crud
from app.models import User

engine = create_engine("sqlite+pysqlite:///data/csctf-portal.sqlite")

with Session(engine) as session:
    # Check if admin user exists
    stmt = select(User).where(User.username == settings.FASTAPI_CSCTF_ADMIN)
    user = session.scalars(stmt).first()
    if user is None:
        print("Creating admin user")
        user = crud.create_user(
            session,
            username=settings.FASTAPI_CSCTF_ADMIN,
            password_hash=settings.FASTAPI_CSCTF_ADMIN_PASSWORD,
            is_admin=True
        )
    else:
        print("Skipping creation of admin user, as it already exists")
    print(user)

    # Check if regular user exists
    stmt = select(User).where(User.username == settings.FASTAPI_CSCTF_USER)
    user = session.scalars(stmt).first()
    if user is None:
        print("Creating regular user")
        user = crud.create_user(
            session,
            username=settings.FASTAPI_CSCTF_USER,
            password_hash=settings.FASTAPI_CSCTF_USER_PASSWORD,
            is_admin=False
        )
    else:
        print("Skipping creation of regular user, as it already exists")
    print(user)
