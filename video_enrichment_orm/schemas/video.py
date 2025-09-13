import uuid
from typing import Optional

from pydantic import Field

from video_enrichment_orm.dao.video import VideoDAO, VideoStatus
from video_enrichment_orm.schemas.timestamps import Timestamps


class VideoBase(Timestamps):
    """Base class for Video schemas to avoid code duplication"""

    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str
    path: str
    extension: str
    frames: Optional[int] = None
    length: Optional[int] = None
    frame_rate: Optional[float] = None
    is_test: Optional[bool] = Field(default=False)
    status: Optional[VideoStatus] = Field(default_factory=lambda: VideoStatus.PENDING)
    status_message: Optional[str] = None


class Video(VideoBase):
    """Full Video schema with ID and UUID for existing videos"""

    id: Optional[int] = None

    @classmethod
    def from_orm(cls, obj: VideoDAO) -> "Video":
        return cls(
            id=obj.id,
            uuid=obj.uuid,
            code=obj.code,
            path=obj.path,
            extension=obj.extension,
            frames=obj.frames,
            length=obj.length,
            frame_rate=obj.frame_rate,
            is_test=obj.is_test,
            status=obj.status,
            status_message=obj.status_message,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class VideoCreate(VideoBase):
    """Video schema for creating new videos without ID"""

    @classmethod
    def to_orm(cls, obj: "VideoCreate") -> VideoDAO:
        """Convert to VideoDAO for database insertion"""
        return VideoDAO(
            uuid=obj.uuid,
            code=obj.code,
            path=obj.path,
            extension=obj.extension,
            frames=obj.frames,
            length=obj.length,
            frame_rate=obj.frame_rate,
            is_test=obj.is_test,
            status=obj.status,
            status_message=obj.status_message,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class VideoUpdate(Timestamps):
    code: Optional[str] = None
    path: Optional[str] = None
    extension: Optional[str] = None
    frames: Optional[int] = None
    length: Optional[int] = None
    frame_rate: Optional[float] = None
    is_test: Optional[bool] = None
    status: Optional[VideoStatus] = None
    status_message: Optional[str] = None
