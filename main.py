import uvicorn as uvi

from fastapi import FastAPI
from ultralytics import YOLO

from src.controllers.register import api_router as register_router
from src.controllers.login import api_router as login_router
from src.controllers.profile import api_router as profile_router
from src.controllers.profile_update import api_router as profile_update_router
from src.controllers.profile_payments import api_router as profile_payments_router
from src.controllers.profile_payments_by_id import api_router as profile_payments_by_id_router
from src.controllers.profile_requests import api_router as profile_requests_router
from src.controllers.profile_requests_by_id import api_router as profile_requests_by_id_router
from src.controllers.support import api_router as support_router
from src.controllers.support_by_id import api_router as support_by_id_router
from src.controllers.predict import api_router as predict_router
from src.misc.logger import logger
from src.misc.lifespan import lifespan
from src.settings.config import load_config
from src.di.setup import setup_di
from src.exceptions.main import register_all_exceptions
from src.services.predictor import Predictor


def include_routers(app: FastAPI):
    app.include_router(register_router)
    app.include_router(login_router)
    app.include_router(profile_router)
    app.include_router(profile_update_router)
    app.include_router(profile_payments_router)
    app.include_router(profile_payments_by_id_router)
    app.include_router(profile_requests_router)
    app.include_router(profile_requests_by_id_router)
    app.include_router(support_router)
    app.include_router(support_by_id_router)
    app.include_router(predict_router)


def build_app():
    logger.info("Starting app")
    app = FastAPI(lifespan=lifespan)
    config = load_config()
    app.state.config = config
    model = YOLO('src/settings/trained_model.pt')
    predictor = Predictor(model)

    setup_di(app, config, predictor)
    include_routers(app)
    register_all_exceptions(app)

    return app


if __name__ == "__main__":
    uvi.run(
        app='main:build_app',
        factory=True,
        host="0.0.0.0",
        port=80,
        # reload=True,
    )
