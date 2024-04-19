from .config import configs
from contextlib import asynccontextmanager
from fastapi import FastAPI
from freenit.config import getConfig

from .api import api

config = getConfig()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if not config.database.is_connected:
        await config.database.connect()
    yield
    if config.database.is_connected:
        await config.database.disconnect()


app = FastAPI(lifespan=lifespan)
app.mount("/api/v1", api)
