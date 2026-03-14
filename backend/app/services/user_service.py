from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user_schema import UserUpdate, UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """Get user detail by ID."""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_in: UserUpdate) -> UserResponse:
        """Update user profile."""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update fields
        if user_in.full_name is not None:
            user.full_name = user_in.full_name

        await self.db.commit()
        await self.db.refresh(user)

        return UserResponse.model_validate(user)
