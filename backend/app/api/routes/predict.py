from fastapi import APIRouter, Response, Depends
from app.schemas.predict_schema import PredictRequest, PredictResponse
from app.services.predict_service import predict_service
from app.helper.base_response import BaseResponse, success_response
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/predict", response_model=BaseResponse[PredictResponse])
def predict_sales(
    request: PredictRequest,
    response: Response,
    current_user: User = Depends(get_current_user),
):
    result = predict_service.get_prediction(
        jumlah_penjualan=request.jumlah_penjualan,
        harga=request.harga,
        diskon=request.diskon,
    )
    return success_response(data=PredictResponse(laris=result))
