from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    location: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str
    mobile: str
    location: str


class LoginRequest(BaseModel):
    emailormbilenumber: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: str
    user: UserResponse