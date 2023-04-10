from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


class Endpoint(BaseModel):
    status: str
    type: str
    rtmpUrl: str
    endpointServiceId: str


class PlayListItem(BaseModel):
    streamUrl: str
    type: str


class VideoStream(BaseModel):
    streamId: str
    status: str
    name: str
    publishType: str
    type: str
    playListStatus: str
    date: Optional[int]
    plannedStartDate: int
    plannedEndDate: int
    duration: int
    endPointList: List[Endpoint]
    playListItemList: List[PlayListItem]
    publicStream: bool
    is360: bool
    listenerHookURL: str
    category: str
    ipAddr: str
    username: str
    password: str
    quality: str
    speed: float
    streamUrl: str
    originAdress: str
    mp4Enabled: int
    webMEnabled: int
    expireDurationMS: int
    rtmpURL: str
    zombi: bool
    pendingPacketSize: int
    hlsViewerCount: int
    dashViewerCount: int
    webRTCViewerCount: int
    rtmpViewerCount: int
    startTime: int
    receivedBytes: int
    bitrate: int
    userAgent: str
    latitude: str
    longitude: str
    altitude: str
    mainTrackStreamId: str
    subTrackStreamIds: List[str]
    absoluteStartTimeMs: int
    webRTCViewerLimit: int
    hlsViewerLimit: int
    dashViewerLimit: int
    subFolder: str
    currentPlayIndex: int
    metaData: str
    playlistLoopEnabled: bool
    updateTime: int

    @validator("date")
    def set_date(cls, _: int):
        return int(datetime.utcnow().strftime("%Y%m%d"))


class VideoStreamRequest(BaseModel):
    video_stream: VideoStream


class VideoStreamResponse(BaseModel):
    video_stream: VideoStream
