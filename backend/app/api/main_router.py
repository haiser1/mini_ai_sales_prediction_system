from fastapi import APIRouter
from app.api.routes import predict, auth, user, sales

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(predict.router, tags=["prediction"])
api_router.include_router(sales.router, tags=["sales"])
