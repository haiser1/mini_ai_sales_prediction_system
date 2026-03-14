from pydantic import BaseModel


class SalesDataResponse(BaseModel):
    id: int
    product_id: str
    product_name: str
    jumlah_penjualan: int
    harga: float
    diskon: int
    status: str

    class Config:
        from_attributes = True


class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
