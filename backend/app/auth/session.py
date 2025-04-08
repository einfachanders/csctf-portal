from cachetools import TTLCache
from fastapi import Request, HTTPException
from jose import jws
from sqlalchemy.orm import Session as DbSession
import uuid

from app.core.config import settings
import app.crud as crud
from app.deps import engine
from app.models import User
from app.schemas.internal import Session

session_cache = TTLCache(
    maxsize=1000,
    ttl=settings.FASTAPI_SESSION_TIMEOUT
)

async def _create_session(user_id: int) -> Session:
    """Creates a new session for a user

    Args:
        user_id (int): ID of the user to create the session for

    Returns:
        Session: Pydantic model of the created session
    """
    while True:
        session_id = str(uuid.uuid4())
        if session_id not in session_cache:
            break
    session = Session(
        session_id=session_id,
        user_id=user_id
    )
    session_cache[session_id] = session
    return session

async def _validate_session(session_id: str) -> Session | None:
    """Checks wether a session is active

    Args:
        session_id (str): ID of the session to verify

    Returns:
        Session|None: Pydantic model of the session, if it is valid.
            None if the session does not exist
    """
    return session_cache.get(session_id)

async def create_cookie(user_id: int) -> str:
    """Creates a signed new session cookie

    Args:
        user_id (int): ID of the user to create the cookie for

    Returns:
        str: signed cookie value
    """
    session = await _create_session(user_id)
    cookie_value = jws.sign(
        payload=session.session_id.encode(),
        key=settings.FASTAPI_JWS_SECRET,
        algorithm="HS256"
    )
    return cookie_value

async def validate_cookie(request: Request) -> Session | None:
    """Checks a request for required cookie and its validity

    Args:
        request (Request): FastAPI Request object

    Raises:
        HTTPException: Raised in case of an error

    Returns:
        Session | None: Pydantic model of the session, if it is valid.
            None if not.
    """
    cookie_value = request.cookies.get(settings.FASTAPI_SESSION_COOKIE_NAME)
    if cookie_value is None:
        raise HTTPException(
            status_code=401,
            detail="Session cookie missing"
        )
    try:
        session_id = jws.verify(
            token=cookie_value,
            key=settings.FASTAPI_JWS_SECRET,
            algorithms=["HS256"]
        ).decode()
        session = await _validate_session(session_id)
        if session is None:
            raise HTTPException(
                status_code=401,
                detail="Session expired or invalid"
            )
        return session
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid session cookie"
        )

async def require_admin_user(request: Request):
    """Ensures the user performing the request has adminstrator access rights

    Args:
        request (Request): FastAPI Request object

    Raises:
        HTTPException: Raised in case of an error
    """
    session = await validate_cookie(request)
    with DbSession(engine) as db_session:
        user = crud.get_user_by_id(db_session, session.user_id)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Unknown user"
            )
        if user.is_admin == False:
            raise HTTPException(
                status_code=403,
                detail="You do not have the required access rights"
            )
