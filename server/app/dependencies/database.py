from typing import Callable, Type
from fastapi import Depends
from starlette.requests import Request
from pymongo.database import Database

from app.db.repositories.base import BaseRepository


def _get_db(request: Request) -> Database:
    return request.app.state.db


def get_repository(
        repo_type: Type[BaseRepository]
) -> Callable[[Database], BaseRepository]:
    def _get_repo(db: Database = Depends(_get_db)) -> BaseRepository:
        return repo_type(db)

    return _get_repo
