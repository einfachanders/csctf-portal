from fastapi import APIRouter, Depends, HTTPException, Response

from app.auth import hash, session
from app.core.config import settings
import app.crud as crud
from app.deps import get_db
from app.exceptions import UnauthorizedException
from app.schemas.api_requests import LoginReq

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
async def admin_login(login_req: LoginReq, db_session = Depends(get_db)):
    user = crud.get_user_by_username(db_session, login_req.username)
    if user is None:
        raise UnauthorizedException(
            message="Invalid credentials"
        )
    if not await hash.verify_password_hash(user.password_hash, login_req.password):
        raise UnauthorizedException(
            message="Invalid credentials"
        )
    cookie_value = await session.create_cookie(user.id)
    response = Response(status_code=200)
    response.set_cookie(
        key=settings.FASTAPI_SESSION_COOKIE_NAME,
        value=cookie_value,
        max_age=settings.FASTAPI_SESSION_TIMEOUT,
        expires=settings.FASTAPI_SESSION_TIMEOUT,
        path="/",
        domain=settings.FASTAPI_DOMAIN,
        secure=True if settings.FASTAPI_PROTOCOL == "https" else False,
        httponly=True,
        samesite="lax"
    )
    return response

@router.get("/check-session", status_code=204)
async def check_session(session = Depends(session.validate_cookie)):
    pass
