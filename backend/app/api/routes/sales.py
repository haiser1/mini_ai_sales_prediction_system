from fastapi import APIRouter, Depends, Query
from app.services.sales_service import SalesService, get_sales_service
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
    sales_service: SalesService = Depends(get_sales_service),
):
    """Get paginated list of sales data with search and filter."""
    items, meta = await sales_service.get_sales_list(
        page=page, limit=limit, search=search, status=status
    )
    return success_response(
        data=[item.model_dump() for item in items],
        message="Sales data retrieved",
        meta=meta.model_dump(),
    )
