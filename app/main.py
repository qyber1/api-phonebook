from fastapi import FastAPI
from app.api import root


def create_app() -> FastAPI:
    app = FastAPI(debug=True)
    app.include_router(root)
    return app





