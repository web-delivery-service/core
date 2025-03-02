from fastapi import FastAPI
import uvicorn

from app.settings.config import settings
from app.api.api_router import api_router


app = FastAPI()
app.include_router(api_router)


def run():
    uvicorn.run(
        app="main:app",
        host=settings.FASTAPI_APP_HOST,
        port=settings.FASTAPI_APP_PORT,
        reload=True,
    )


if __name__ == "__main__":
    run()
