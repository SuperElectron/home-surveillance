from pprint import pprint
import pytest

from fastapi import FastAPI
from starlette import status
from httpx import AsyncClient

from app.models.video_stream import VideoStreamRequest, VideoStreamResponse

pytestmark = pytest.mark.asyncio

POST_STREAM_ROUTE = "stream:create-stream"

async def test_create_stream(
    app: FastAPI,
    client: AsyncClient,
    stream_request: VideoStreamRequest
) -> None:

    response = await client.post(
        app.url_path_for(POST_STREAM_ROUTE),
        json=stream_request.dict() 
    )

    assert response.status_code == status.HTTP_201_CREATED

    stream_response = VideoStreamResponse(**response.json())

    assert stream_response.video_stream.streamId == stream_request.video_stream.streamId
    assert stream_response.video_stream.name == stream_request.video_stream.name
    
async def test_create_stream_unprocessable(app: FastAPI, client: AsyncClient) -> None:

    pprint(app.url_path_for(POST_STREAM_ROUTE))

    response = await client.post(
    app.url_path_for(POST_STREAM_ROUTE),
        json={"bad_request": "bad"}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_duplicate_stream(
    app: FastAPI, 
    client: AsyncClient,
    stream_request: VideoStreamRequest
) -> None: 
        await client.post(
            app.url_path_for(POST_STREAM_ROUTE),
            json=stream_request.dict() 
        )

        response = await client.post(
            app.url_path_for(POST_STREAM_ROUTE),
            json=stream_request.dict() 
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

