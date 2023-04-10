from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.core.events import create_startup_handler, create_shutdown_handler


def get_application() -> FastAPI:
    load_dotenv()

    application = FastAPI(
        title=PROJECT_NAME,
        debug=DEBUG,
        version=VERSION
    )

    if DEBUG:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )

    application.add_event_handler("startup", create_startup_handler(application))
    application.add_event_handler("shutdown", create_shutdown_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX)

    return application


app = get_application()
