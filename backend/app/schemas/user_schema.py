from pydantic import BaseModel


class UserUpdate(BaseModel):
    full_name: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str

    class Config:
        from_attributes = True
