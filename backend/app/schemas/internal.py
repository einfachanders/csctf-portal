from datetime import tzinfo, datetime, timedelta
from pydantic import BaseModel, Field
import uuid

from app.core.config import settings

class Session(BaseModel):
    # use a uuid stored as string cause some python
    # libraries cannot handle uuid very well
    session_id: str = Field(description="Session ID")
    user_id: int = Field(description="ID of the user who started the session")
    created: datetime = Field(
        default=datetime.now(),
        description="Timestamp of session creation"
    )
    valid_until: datetime = Field(
        default=datetime.now() + timedelta(seconds=settings.FASTAPI_SESSION_TIMEOUT),
        description="Timestamp until the session is valid"
    )
