import logging

from fastapi import FastAPI
from app.api import root


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    app = FastAPI()
    app.include_router(root)
    return app





