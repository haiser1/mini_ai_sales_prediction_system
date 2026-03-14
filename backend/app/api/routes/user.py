from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserUpdate, UserResponse
from app.services.user_service import UserService
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.helper.base_response import BaseResponse, success_response

router = APIRouter()


@router.get("/me", response_model=BaseResponse)
async def get_current_user_detail(
    current_user: User = Depends(get_current_user),
):
    """Get the profile of the currently authenticated user."""
    # Langsung pakai current_user dari dependency, tidak perlu query lagi
    user_data = UserResponse.model_validate(current_user)
    return success_response(
        data=user_data.model_dump(), message="User detail retrieved"
    )


@router.put("/me", response_model=BaseResponse)
async def update_current_user(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update the profile of the currently authenticated user."""
    user_service = UserService(db)
    user = await user_service.update_user(current_user.id, user_in)
    return success_response(data=user.model_dump(), message="User updated successfully")
