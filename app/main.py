from fastapi import Request, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from app.functions.env import EnvVars
from app.messageRPC import Client
from app.routes import *


system_variables = EnvVars()  # load in config file

# Initialize logging
logging.basicConfig(
    level=(
        logging.DEBUG if system_variables.debug else logging.INFO
    ),
    format='\033[31m%(levelname)s\033[0m \033[90min\033[0m \033[33m%(filename)s\033[0m \033[90mon\033[0m %(asctime)s\033[90m:\033[0m %(message)s',
    datefmt='\033[32m%m/%d/%Y\033[0m \033[90mat\033[0m \033[32m%H:%M:%S\033[0m'
)
logging.getLogger("fastapi").setLevel(logging.ERROR)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.ERROR)
logging.getLogger(__name__)
if system_variables.debug:
    logging.info("static.env - 'DEBUG' key found. Running in debug mode, do not use in production.")


def create_app():
    new_app = FastAPI(
        title="ITP API",
        description="ITP API Service",
        docs_url="/internaldocs",
        redoc_url="/docs"
    )
    # new_app.mq = Client(system_variables.mq_uri)

    # Startup and Shutdown Events
    @new_app.on_event("startup")
    async def startup():
        new_app.mq = Client(system_variables.mq_uri)
        await new_app.mq.connect()

    # @new_app.on_event("shutdown")
    # async def shutdown():

    # Add cors
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    new_app.include_router(
        session_router,
        prefix="/session",
        tags=["session"]
    )

    # Routes
    new_app.include_router(
        user_router,
        prefix="/user",
        tags=["user"]
    )

    def custom_openapi():
        if new_app.openapi_schema:
            return new_app.openapi_schema
        openapi_schema = get_openapi(
            title="Cloneflix",
            description="idk",
            version="Alpha: 1.0.0",
            routes=new_app.routes,
            tags=[
                {
                    "name": "Session",
                    "description": "User session management"
                },
            ]
        )
        new_app.openapi_schema = openapi_schema
        return new_app.openapi_schema

    new_app.openapi = custom_openapi

    # Include Routes
    return new_app


app = create_app()
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=2000)


