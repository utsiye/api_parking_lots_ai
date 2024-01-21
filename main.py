import uvicorn
import asyncio

from fastapi import FastAPI

from app.misc.logger import logger
from app.routers.register import api_router as register_router
from app.routers.login import api_router as login_router
from app.misc.di.setup import setup_di
from app.misc.lifespan import lifespan
from app.settings.config import load_config


def include_all_routers(app: FastAPI):
    app.include_router(register_router)
    app.include_router(login_router)
    ...

async def main() -> FastAPI:
    logger.info("Starting app")

    app = FastAPI(lifespan=lifespan)

    include_all_routers(app)

    config = load_config()
    setup_di(app, config)

    return app


if __name__ == '__main__':
    try:
        app = asyncio.run(main())
        uvicorn.run(app, host="0.0.0.0", port=80)
    except (KeyboardInterrupt, SystemExit):
        logger.error("API was stopped")
