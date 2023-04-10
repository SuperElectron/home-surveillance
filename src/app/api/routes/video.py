from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from httpx import HTTPStatusError, TimeoutException

from app.models.video_stream import VideoStreamRequest, VideoStreamResponse, VideoStream
from app.resources.video_constants import TAG_VIDEO, AMS_TIMEOUT, AMS_UNAVAILABLE, AMS_DUPLICATE
from app.dependencies.http_client import get_client_service
from app.services.video_stream_service import VideoStreamService

router = APIRouter()


@router.post(
    "",
    name="stream:create-stream",
    tags=[TAG_VIDEO],
    response_class=JSONResponse,
    response_model=VideoStreamResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_stream(
        stream_request: VideoStreamRequest,
        client_service: VideoStreamService = Depends(
            get_client_service
        )
) -> VideoStreamResponse:
    stream: VideoStream = stream_request.video_stream
    result: VideoStream = await client_service.create_stream(stream)

    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=AMS_DUPLICATE)

    if isinstance(result, HTTPStatusError):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=AMS_UNAVAILABLE)

    if isinstance(result, TimeoutException):
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail=AMS_TIMEOUT)

    return VideoStreamResponse(video_stream=result)
