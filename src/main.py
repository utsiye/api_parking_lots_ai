import uvicorn as uvi

from fastapi import FastAPI

from controllers.register import api_router as register_router
from controllers.login import api_router as login_router
from misc.logger import logger
from misc.lifespan import lifespan
from settings.config import load_config
from di.setup import setup_di


def include_routers(app: FastAPI):
    app.include_router(register_router)
    app.include_router(login_router)

def build_app():
    logger.info("Starting app")
    app = FastAPI(lifespan=lifespan)
    config = load_config()
    app.state.config = config

    setup_di(app, config)
    include_routers(app)

    return app


if __name__ == "__main__":
    uvi.run(
        app='src.main:build_app',
        factory=True,
        host="0.0.0.0",
        port=80,
        tracemalloc=True
        # reload=True,
    )
