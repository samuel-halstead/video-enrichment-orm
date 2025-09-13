import uuid
from typing import Optional

from pydantic import Field

from video_enrichment_orm.dao.segment_detection import SegmentDetectionDAO
from video_enrichment_orm.schemas.timestamps import Timestamps


class SegmentDetectionBase(Timestamps):
    """Base class for SegmentDetection schemas to avoid code duplication"""

    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    video_id: int
    start_frame: int
    end_frame: int
    taxonomy_id: int
    entity_id: int


class SegmentDetection(SegmentDetectionBase):
    """Full SegmentDetection schema with ID and UUID for existing segment detections"""

    id: Optional[int] = None

    @classmethod
    def from_orm(cls, obj: SegmentDetectionDAO) -> "SegmentDetection":
        return cls(
            id=obj.id,
            uuid=obj.uuid,
            video_id=obj.video_id,
            start_frame=obj.start_frame,
            end_frame=obj.end_frame,
            taxonomy_id=obj.taxonomy_id,
            entity_id=obj.entity_id,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class SegmentDetectionCreate(SegmentDetectionBase):
    """SegmentDetection schema for creating new segment detections without ID"""

    @classmethod
    def to_orm(cls, obj: "SegmentDetectionCreate") -> SegmentDetectionDAO:
        """Convert to SegmentDetectionDAO for database insertion"""
        return SegmentDetectionDAO(
            uuid=obj.uuid,
            video_id=obj.video_id,
            start_frame=obj.start_frame,
            end_frame=obj.end_frame,
            taxonomy_id=obj.taxonomy_id,
            entity_id=obj.entity_id,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class SegmentDetectionUpdate(Timestamps):
    start_frame: Optional[int] = None
    end_frame: Optional[int] = None
