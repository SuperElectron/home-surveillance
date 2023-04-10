from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from starlette import status

from app.db.repositories.backup_repository import BackupRepository
from app.dependencies.database import get_repository

from app.models.backup import BackupResponse, BackupListResponse
from app.resources.backup_constants import (
    TAG_BACKUP,
    QUERY_BACKUP_SORT_REGEX,
    QUERY_BACKUP_FILTER_REGEX,
    QUERY_BACKUP_DEFAULT_LIMIT,
    QUERY_BACKUP_DEFAULT_OFFSET,
)

router = APIRouter()


@router.get(
    "",
    name="backup:get-backups",
    tags=[TAG_BACKUP],
    response_class=JSONResponse,
    response_model=BackupListResponse
)
async def get_backups(
        limit: int = Query(
            QUERY_BACKUP_DEFAULT_LIMIT,
            alias="limit",
            description="Backups per page"
        ),
        offset: int = Query(
            QUERY_BACKUP_DEFAULT_OFFSET,
            alias="offset",
            description="Pagination offset"
        ),
        sort_params: Optional[List[str]] = Query(
            None,
            alias="sort",
            description="Sorting for collection",
            regex=QUERY_BACKUP_SORT_REGEX
        ),
        filters: Optional[List[str]] = Query(
            None,
            alias="filters",
            description="Filters for collection",
            regex=QUERY_BACKUP_FILTER_REGEX
        ),
        backup_repository: BackupRepository = Depends(
            get_repository(BackupRepository)
        )
) -> BackupListResponse:
    if sort_params:
        sort_param_list = [sort_param.split(":") for sort_param in sort_params]
        sort_params = {sort_param[0]: sort_param[1] for sort_param in sort_param_list}

    if filters:
        filter_param_list = [filter_param.split(":") for filter_param in filters]
        filters = {filter_param[0]: filter_param[1] for filter_param in filter_param_list}

    backups = backup_repository.find_all(offset, limit, sort_params, filters)

    return BackupListResponse(backups=backups)


@router.get(
    "/{id}",
    name="backup:get-one-backup",
    tags=[TAG_BACKUP],
    response_class=JSONResponse,
    response_model=BackupResponse
)
async def get_one_backup(
        id: str,
        backup_repository: BackupRepository = Depends(get_repository(BackupRepository))
) -> BackupResponse:
    result = await backup_repository.find_one_backup(id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )

    return BackupResponse(backup=result)
