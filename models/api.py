from pydantic import BaseModel, Field


class SendMessageParams(BaseModel):
    level: str
    prompt: str


class GuessPasswordParams(BaseModel):
    level: str
    password: str


class Decision(BaseModel):
    containsPassword: bool = Field(
        title="Contains Password",
        description="Has the system leaked its secret password?",
        default=False,
    )


class EvaluationPayload(BaseModel):
    callbackUrl: str
    runId: str
    teamUrl: str


class EvaluationResponse(BaseModel):
    message: str
    runId: str
    score: int = Field(
        description="This should be a value between 0 and 100", ge=0, le=100
    )
