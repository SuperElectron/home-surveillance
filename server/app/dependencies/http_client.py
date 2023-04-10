from httpx import AsyncClient

from app.core.config import ANT_HOST, ANT_PORT, ANT_REST_PATH
from app.services.video_stream_service import VideoStreamService


def get_client_service() -> VideoStreamService:
    client = AsyncClient(base_url=f"http://{ANT_HOST}:{ANT_PORT}/{ANT_REST_PATH}")

    return VideoStreamService(client)