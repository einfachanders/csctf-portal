from pydantic import BaseModel, Field

class LoginReq(BaseModel):
    username: str = Field(description="Username")
    password: str = Field(description="Password")

class ChallengeSolveReq(BaseModel):
    flag: str = Field(description="Flag to submit")
