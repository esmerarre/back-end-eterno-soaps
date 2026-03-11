from pydantic import BaseModel, Field


# Request body for creating a new admin account.
class AdminCreate(BaseModel):
    username: str
    # Basic minimum length guard; hash happens in the route/service layer.
    password: str = Field(min_length=8)


# Request body for login.
class AdminLogin(BaseModel):
    username: str
    password: str


# Response body returned after successful login.
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str | None = None


# Safe admin response shape (never includes password/hash fields).
class AdminOut(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}