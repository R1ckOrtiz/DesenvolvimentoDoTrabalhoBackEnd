from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(..., examples=["admin@raizes.com"])
    senha: str = Field(..., min_length=6, examples=["admin123"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    perfil: str
