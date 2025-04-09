from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings
from app.exceptions import GenericJSONException

# init FastAPI application
app = FastAPI(
    title=settings.FASTAPI_PROJECT_NAME,
    openapi_url=f"{settings.FASTAPI_BASE_URI}/openapi.json",
    docs_url=f"{settings.FASTAPI_BASE_URI}/docs"
)

# Set all CORS enabled origins
if settings.FASTAPI_BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.FASTAPI_BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["GET", "PATCH", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

app.include_router(
    api_router,
    prefix=settings.FASTAPI_BASE_URI
)

@app.exception_handler(GenericJSONException)
async def generic_exception_handler(request: Request, excep: GenericJSONException):
    return JSONResponse(
        status_code=excep.status_code,
        content=excep.json
    )