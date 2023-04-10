from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime


class Backup(BaseModel):
    _id: ObjectId
    stream_id: str 
    file_path: str
    external_filepath: str
    created_at: datetime
    duration: Optional[str]
    start: Optional[str]
    bitrate: Optional[str]

class BackupRequest(BaseModel):
    pass

class BackupResponse(BaseModel):
    backup: Backup

class BackupListResponse(BaseModel):
    backups: List[Backup]