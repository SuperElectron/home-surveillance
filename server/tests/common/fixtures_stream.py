from ast import List
import pytest
import random

from mimesis.random import Random
from mimesis import Internet

from app.models.video_stream import (
    VideoStreamRequest, 
    VideoStream, 
    Endpoint, 
    PlayListItem
)

@pytest.fixture
def stream_request(random_generator: Random, internet: Internet) -> VideoStreamRequest:
    endpoint_statuses: List[str] = ["started", "finished", "failed", "broadcasting"]
    endpoint_types: List[str] = ["facebook", "periscope", "youtube", "generic"]
    stream_statuses: List[str] = ["finished", "broadcasting", "created"]
    stream_types = ["liveStream", "ipCamera", "streamSource", "VoD", "playlist"] 
    publishType: List[str] = ["WebRTC", "RTMP", "Pull"]
    int_options: List[int] = [-1, 0, 1]
    stream_qualities: List[str] = ["360p", "480p", "720p", "1080p"]

    endpoints: List[Endpoint] = [
        Endpoint(
            status=random.choice(endpoint_statuses), 
            type=random.choice(endpoint_types),
            rtmpUrl=generate_url("rtmp"),
            endpointServiceId=random_generator.randstr()
        )
    for _ in range(random.randint(1, 200))] 
    
    playlists: List[PlayListItem] = [
        PlayListItem(
            streamUrl=generate_url("http"),
            type=random_generator.randstr()
        )
    for _ in range(random.randint(1, 200))]

    stream_model: VideoStream = VideoStream(
        streamId=random_generator.randstr(),
        status=random.choice(stream_statuses),
        playListStatus=random.choice(stream_statuses),
        type=random.choice(stream_types),
        publishType=random.choice(publishType),
        name=random_generator.randstr(),
        description=random_generator.randstr(),
        publish=bool(random.getrandbits(1)),
        plannedStartDate=0,
        plannedEndDate=0,
        duration=random.randint(1, 600),
        endPointList=endpoints,
        playListItemList=playlists,
        is360=bool(random.getrandbits(1)),
        listenerHookURL=generate_url("http"),
        ipAddr=internet.ip_v4(),
        username=random_generator.randstr(),
        password=random_generator.randstr(),
        quality=random.choice(stream_qualities),
        originAdress=internet.ip_v4(),
        mp4Enabled=random.choice(int_options),
        webMEnabled=random.choice(int_options),
        expireDurationMS=random.randint(0, 600),
        rtmpURL=generate_url("rtmp"),
        rtmpViewerCount=random.randint(0, 600),
        category=random_generator.randstr(),
        speed=random.randint(0, 600),
        streamUrl=generate_url("http"),
        publicStream=bool(random.getrandbits(1)),
        zombi=bool(random.getrandbits(1)),
        pendingPacketSize=random.randint(0, 600),
        hlsViewerCount=random.randint(0, 600),
        dashViewerCount=random.randint(0, 600),
        webRTCViewerCount=random.randint(0, 600),
        startTime=random.randint(0, 600),
        receivedBytes=random.randint(0, 600),
        bitrate=random.randint(0, 600),
        userAgent=internet.user_agent(),
        latitude=str(random.random()),
        longitude=str(random.random()),
        altitude=random.randint(0, 600),
        mainTrackStreamId=random_generator.randstr(),
        subTrackStreamIds= [random_generator.randstr() for _ in range(1, 200)],
        absoluteStartTimeMs=random.randint(0, 600),
        webRTCViewerLimit=random.randint(0, 600),
        hlsViewerLimit=random.randint(0, 600),
        dashViewerLimit=random.randint(0, 600),
        subFolder=random_generator.randstr(),
        currentPlayIndex=random.randint(0, 600),
        metaData=random_generator.randstr(),
        playlistLoopEnabled=bool(random.getrandbits(1)),
        updateTime=random.randint(0, 600)
    )

    return VideoStreamRequest(video_stream=stream_model)

def generate_url(type: str) -> str:
    random_generator = Random()
    return f"{type}://{random_generator.randstr()}.{random_generator.randstr()}.com/{random_generator.randstr()}"