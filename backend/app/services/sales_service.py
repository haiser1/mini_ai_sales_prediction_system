import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.sales_data import SalesData
from app.schemas.sales_schema import SalesDataResponse, PaginationMeta


class SalesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_sales_list(
        self,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        status: str | None = None,
    ) -> tuple[list[SalesDataResponse], PaginationMeta]:
        """Get paginated list of sales data with optional search and filter."""
        query = select(SalesData)
        count_query = select(func.count(SalesData.id))
        # Search filter: search by product_id or product_name
        if search:
            search_filter = or_(
                SalesData.product_id.ilike(f"%{search}%"),
                SalesData.product_name.ilike(f"%{search}%"),
            )
            query = query.filter(search_filter)
            count_query = count_query.filter(search_filter)
        # Status filter: "Laris" or "Tidak"
        if status:
            query = query.filter(SalesData.status == status)
            count_query = count_query.filter(SalesData.status == status)
        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        # Pagination
        total_pages = math.ceil(total / limit) if total > 0 else 1
        offset = (page - 1) * limit
        query = query.order_by(SalesData.id).offset(offset).limit(limit)
        result = await self.db.execute(query)
        items = result.scalars().all()

        data = [SalesDataResponse.model_validate(item) for item in items]
        meta = PaginationMeta(
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )
        return data, meta
