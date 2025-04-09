from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.settings.config import settings
from app.api.api_router import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*settings.BACKEND_CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=[*settings.BACKEND_CORS_METHODS.split(",")],
    allow_headers=[*settings.BACKEND_CORS_HEADERS.split(",")],
)

# app.add_api_route(
#     path="/hello",
#     endpoint=hello_world,
#     methods=["GET"],
#     response_model=dict,
#     summary="Стандартное приветствие"
# )


def run():
    uvicorn.run(
        app="main:app",
        host=settings.FASTAPI_APP_HOST,
        port=settings.FASTAPI_APP_PORT,
        reload=True,
    )


if __name__ == "__main__":
    run()
