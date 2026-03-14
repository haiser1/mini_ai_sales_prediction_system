from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.sales_service import SalesService
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.helper.base_response import BaseResponse, success_response

router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def get_sales_list(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str | None = Query(
        None, description="Search by product_id or product_name"
    ),
    status: str | None = Query(None, description="Filter by status: Laris or Tidak"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated list of sales data with search and filter."""
    sales_service = SalesService(db)
    items, meta = await sales_service.get_sales_list(
        page=page, limit=limit, search=search, status=status
    )
    return success_response(
        data=[item.model_dump() for item in items],
        message="Sales data retrieved",
        meta=meta.model_dump(),
    )
