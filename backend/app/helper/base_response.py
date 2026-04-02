from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel

DataType = TypeVar("DataType")


class BaseResponse(BaseModel, Generic[DataType]):
    message: str
    data: Optional[DataType] = None
    meta: Optional[Dict[str, Any]] = None



def success_response(
    data: Any = None, message: str = "Success", meta: Optional[dict] = None
) -> dict:
    """Helper to return a success response dictionary."""
    response: dict = {"message": message}
    if data is not None:
        response["data"] = data
    if meta is not None:
        response["meta"] = meta
    return response


def error_response(message: str, details: Any = None) -> dict:
    """Helper to return an error response dictionary."""
    response: dict = {"message": message}
    if details is not None:
        response["details"] = details
    return response
