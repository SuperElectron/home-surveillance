from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

class Backup(BaseModel):
    _id: Optional[ObjectId]
    stream_id: str
    file_path: str
    external_filepath: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    duration: Optional[str]
    start: Optional[str] 
    bitrate: Optional[str]

    