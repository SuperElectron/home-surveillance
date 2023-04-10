from pymongo.database import Collection
from loguru import logger

from app.models.backup import Backup

class BackupRepository(): 

    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def insert_one(self, backup: Backup) -> Backup:
        try: 
            self._collection.insert_one(backup.dict())
            return Backup
        except Exception as e:
            logger.error(e)
