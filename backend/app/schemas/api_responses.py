from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ChallengeResp(BaseModel):
    id: int = Field(description="Challenge ID")
    name: str = Field(description="Challenge Name")
    story: str = Field(description="Challenge Story")
    description: str = Field(description="Challenge Description")
    difficulty: str = Field(description="Challenge Difficulty")
    filename: Optional[str] = Field(default="", description="Name of the file associated with the challenge")
    solved: bool = Field(description="Solve state of Challenge")
    solved_timestamp: Optional[datetime] = Field(
        default=None,
        description="Time of challenge solving"
    )
