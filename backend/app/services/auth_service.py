from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.auth_schema import UserCreate, UserLogin, TokenResponse
from app.models.user import User
from app.helper.password_helper import get_password_hash, verify_password
from app.helper.token_helper import create_access_token, create_refresh_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, user_in: UserCreate) -> UserCreate:
        # Check if email exists
        result = await self.db.execute(select(User).filter(User.email == user_in.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already registered")

        # Create new user
        hashed_password = get_password_hash(user_in.password)
        new_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        # Generate tokens

        return UserCreate(
            email=user_in.email, password=user_in.password, full_name=user_in.full_name
        )

    async def login(self, user_in: UserLogin) -> TokenResponse:
        # Find user by email
        result = await self.db.execute(select(User).filter(User.email == user_in.email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        # Verify password
        if not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        return TokenResponse(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
