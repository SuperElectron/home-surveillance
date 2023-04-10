from typing import Dict, List, Union
from pymongo.database import Database
from bson import ObjectId

from app.db.repositories.base import BaseRepository
from app.models.backup import Backup
from app.utils.sync import run_in_thread


class BackupRepository(BaseRepository):

    def __init__(self, db: Database) -> None:
        self._db = db

    async def find_one_backup(self, id: str) -> Union[Backup, None]:
        query = {"_id": ObjectId(id)}
        backup = await run_in_thread(self._db.backups.find_one, query)

        if backup:
            return Backup(**backup)

        return backup

    def find_all(
            self,
            offset: int,
            limit: int,
            sort_params: Dict[str, str] = None,
            filters: List[str] = None
    ) -> List[Backup]:
        backups = []

        if sort_params and not filters:
            query = self._add_sorting(sort_params)
            results = self._db.backups.find().skip(offset).limit(limit).sort(query)
        elif filters and not sort_params:
            pass
        elif filters and sort_params:
            query = self._add_sorting(sort_params)
        else:
            results = self._db.backups.find().skip(offset).limit(limit)

        for result in results:
            backups.append(result)

        return backups
