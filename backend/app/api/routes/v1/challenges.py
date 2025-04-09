from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import session
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
