import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
from app.api.main_router import api_router
from app.helper.base_response import error_response
from app.helper.logger import json_logger
from app.services.predict_service import load_ml_models, clear_ml_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executed at startup
    load_ml_models()
    yield
    # Executed on shutdown
    clear_ml_models()


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = [
            {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content=error_response(message="Validation Error", details=errors),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code, content=error_response(message=str(exc.detail))
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        json_logger.error(
            "Unhandled Server Error",
            exc_info=exc,
            extra={"url": request.url.path, "method": request.method},
        )
        return JSONResponse(
            status_code=500,
            content=error_response(message="Internal Server Error", details=str(exc)),
        )


def register_middlewares(app: FastAPI):
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.middleware("http")
    async def log_requests_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        log_dict = {
            "url": request.url.path,
            "method": request.method,
            "process_time_sec": round(process_time, 4),
            "status_code": response.status_code,
            "client_ip": request.client.host if request.client else None,
        }

        if response.status_code >= 500:
            json_logger.error("Request Failed with Server Error", extra=log_dict)
        elif response.status_code >= 400:
            json_logger.warning("Client Error Request", extra=log_dict)
        else:
            json_logger.info("Request Processed Successfully", extra=log_dict)

        return response


def create_app() -> FastAPI:
    """
    Application Factory: Membangun instance FastAPI.
    Berguna untuk Unit Testing agar tidak ada state/cache global yang terbawa.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    register_middlewares(app)
    register_exception_handlers(app)

    # Register Routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/")
    def root():
        return {"message": f"Welcome to {settings.PROJECT_NAME}", "docs_url": "/docs"}

    return app


app = create_app()
