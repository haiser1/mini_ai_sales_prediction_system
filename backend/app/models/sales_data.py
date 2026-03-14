from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class SalesData(Base):
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(String, unique=True, index=True, nullable=False)
    product_name = Column(String, index=True, nullable=False)
    jumlah_penjualan = Column(Integer, nullable=False)
    harga = Column(Float, nullable=False)
    diskon = Column(Integer, nullable=False, default=0)
    status = Column(String, index=True, nullable=False)
