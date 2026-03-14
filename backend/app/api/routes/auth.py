from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schema import UserCreate, UserLogin
from app.services.auth_service import AuthService
from app.core.database import get_db
from app.helper.base_response import BaseResponse, success_response

router = APIRouter()

@router.post("/register", response_model=BaseResponse)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    token_response = await auth_service.register(user_in)
    return success_response(
        data=token_response.model_dump(), 
        message="User registered successfully"
    )

@router.post("/login", response_model=BaseResponse)
async def login_user(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    token_response = await auth_service.login(user_in)
    return success_response(
        data=token_response.model_dump(), 
        message="Login successful"
    )
