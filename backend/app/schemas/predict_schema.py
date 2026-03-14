from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    jumlah_penjualan: int = Field(..., description="Jumlah unit terjual", ge=0)
    harga: int = Field(..., description="Harga produk", ge=0)
    diskon: int = Field(..., description="Persentase diskon (0-100)", ge=0, le=100)


class PredictResponse(BaseModel):
    laris: str = Field(..., description="Status prediksi (Laris / Tidak)")
