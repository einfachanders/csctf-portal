from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
import pathlib
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import session
from app.core.config import settings
import app.crud as crud
from app.deps import get_db
from app.exceptions import BadRequestException, NotFoundException
from app.models import Challenge
from app.schemas.api_requests import ChallengeSolveReq
from app.schemas.api_responses import ChallengeResp

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"],
    # ensures that every request made to the router
    # must have a valid session
    dependencies=[Depends(session.validate_cookie)]
)

@router.get("", status_code=200, response_model=list[ChallengeResp])
async def get_challenges(db_session: Session = Depends(get_db)):
    stmt = select(Challenge)
    db_challenges = db_session.scalars(stmt).all()
    return db_challenges

@router.post("/{id}/solve", status_code=200, response_model=ChallengeResp)
async def solve_challenge(id: int, req: ChallengeSolveReq, db_session: Session = Depends(get_db)):
    stmt = select(Challenge.flag).where(Challenge.id == id)
    db_flag = db_session.scalars(stmt).first()
    if db_flag is None:
        raise NotFoundException(
            message=f"Challenge {id} not found"
        )
    if db_flag == req.flag:
        db_challenge = crud.update_challenge(
            db=db_session,
            challenge_id=id,
            solved=True,
            solved_timestamp=datetime.now(timezone.utc)
        )
        return db_challenge
    else:
        raise BadRequestException(
            message="Incorrect flag"
        )

@router.get("/{id}/download", status_code=200, response_class=FileResponse)
async def download_challenge_data(id: int, db_session: Session = Depends(get_db)):
    stmt = select(Challenge).where(Challenge.id == id)
    db_challenge = db_session.scalars(stmt).first()
    if db_challenge is None:
        raise NotFoundException(
            message=f"Challenge {id} not found"
        )
    if db_challenge.filename is None:
        raise NotFoundException(
            message=f"Challenge {id} has no associated file"
        )
    if not (settings.BACKEND_DIR / "files" / db_challenge.filename).is_file():
        raise NotFoundException(
            message=f"File for challenge {id} not found"
        )
    return FileResponse(
        settings.BACKEND_DIR / "files" / db_challenge.filename,
        filename=db_challenge.filename
    )
