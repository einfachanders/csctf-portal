import json
import pathlib
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
import app.crud as crud
from app.models import User

engine = create_engine("sqlite+pysqlite:///data/csctf-portal.sqlite")

with Session(engine) as session:
    # Check if regular user exists
    stmt = select(User).where(User.username == settings.FASTAPI_CSCTF_USER)
    user = session.scalars(stmt).first()
    if user is None:
        print("Creating csp11 user")
        user = crud.create_user(
            session,
            username=settings.FASTAPI_CSCTF_USER,
            password_hash=settings.FASTAPI_CSCTF_USER_PASSWORD,
            is_admin=False
        )
    else:
        print("Skipping creation of csp11 user, as it already exists")

    challenges_path = pathlib.Path("data/challenges.json")
    if not challenges_path.exists():
        raise FileNotFoundError("data/challenges.json not found. Please provie it.")
    else:
        with open(challenges_path, "r") as infile:
            challenges = json.load(infile)
        for challenge in challenges:
            db_challenge = crud.get_challenge_by_id(session, challenge["id"])
            if db_challenge is None:
                print(f"Challenge {challenge["id"]} not stored in database, creating it")
                db_challenge = crud.create_challenge(session, **challenge)
            else:
                print(f"Challenge {challenge["id"]} already present in database, skipping creation")
