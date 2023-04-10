import pytest
import pytest_asyncio
import docker as libdocker

from mimesis.random import Random
from mimesis import Internet
from os import environ, getenv
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pymongo.database import Database

ANT_DOCKER_IMAGE: str = "antmediaserver"
ANT_DOCKER_CONTAINER_NAME: str = "test-antmedia"
MONGO_DOCKER_IMAGE: str = "mongo"
MONGO_DOCKER_CONTAINER_NAME: str = "test-mongo"

USE_LOCAL_MONGO: bool = getenv("USE_LOCAL_MONGO", False)

pytest_plugins = ["tests.common.fixtures_stream"]


@pytest.fixture(scope="session")
def docker() -> libdocker.APIClient:
    with libdocker.APIClient(version="auto") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def mongo_server(docker: libdocker.APIClient) -> None:
    if USE_LOCAL_MONGO is not False:
        host_config = docker.create_host_config(port_bindings={27017: 27017})
        container = docker.create_container(
            image=MONGO_DOCKER_IMAGE,
            name=MONGO_DOCKER_CONTAINER_NAME,
            detach=True,
            ports=[27017],
            host_config=host_config
        )

        docker.start(container=container["Id"])
        docker.start(container=container["Id"])
        inspection = docker.inspect_container(container["Id"])
        host = inspection["NetworkSettings"]["IPAddress"]

        environ["DB_HOST"] = host
        environ["DB_USER"] = "root"
        environ["DB_PASSWORD"] = "admin"
        environ["DB_NAME"] = "backup_db"
        environ["DB_PORT"] = "27017"

        yield container
        docker.kill(container["Id"])
        docker.remove_container(container["Id"])
    else:
        yield
        return


@pytest.fixture
def app() -> FastAPI:
    from main import get_application

    return get_application()


@pytest_asyncio.fixture
async def initialized_app(app: FastAPI):
    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture
async def client(initialized_app: FastAPI):
    async with AsyncClient(
            app=initialized_app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def db(initialized_app: FastAPI) -> Database:
    return initialized_app.state.db


@pytest.fixture
def random_generator() -> Random:
    return Random()


@pytest.fixture
def internet() -> Internet:
    return Internet()
