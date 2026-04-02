from fastapi import APIRouter, Depends
from app.schemas.auth_schema import UserCreate, UserLogin
from app.services.auth_service import AuthService, get_auth_service
from app.helper.base_response import BaseResponse, success_response

router = APIRouter()

@router.post("/register", response_model=BaseResponse)
async def register_user(user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    token_response = await auth_service.register(user_in)
    return success_response(
        data=token_response.model_dump(), 
        message="User registered successfully"
    )

@router.post("/login", response_model=BaseResponse)
async def login_user(user_in: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    token_response = await auth_service.login(user_in)
    return success_response(
        data=token_response.model_dump(), 
        message="Login successful"
    )
