from cachetools import TTLCache
from fastapi import Request, HTTPException
from jose import jws
import uuid

from app.core.config import settings
from app.exceptions import UnauthorizedException
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
        raise UnauthorizedException(
            message="Session cookie missing"
        )
    try:
        session_id = jws.verify(
            token=cookie_value,
            key=settings.FASTAPI_JWS_SECRET,
            algorithms=["HS256"]
        ).decode()
        session = await _validate_session(session_id)
        if session is None:
            raise UnauthorizedException(
                message="Session expired or invalid"
            )
        return session
    except Exception:
        raise UnauthorizedException(
            message="Invalid session cookie"
        )
