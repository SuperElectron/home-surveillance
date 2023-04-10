from pydantic import BaseModel

from app.api.watcher import Watcher

# class ProducerInitMsg(BaseModel):
#     watcher: Watcher

class ProducerExitMsg(BaseModel):
    msg: str