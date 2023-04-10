from fastapi import APIRouter

from app.api.routes import video
from app.api.routes import backup
from app.resources.video_constants import TAG_VIDEO
from app.resources.backup_constants import TAG_BACKUP

router = APIRouter()

router.include_router(video.router, tags=[TAG_VIDEO], prefix="/stream")
router.include_router(backup.router, tags=[TAG_BACKUP], prefix="/backup")
