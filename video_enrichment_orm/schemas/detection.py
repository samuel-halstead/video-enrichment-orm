import uuid
from typing import Optional

from pydantic import Field

from video_enrichment_orm.dao.detection import DetectionDAO
from video_enrichment_orm.schemas.timestamps import Timestamps


class DetectionBase(Timestamps):
    """Base class for Detection schemas to avoid code duplication"""

    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    video_id: int
    frame: int
    segment_detection_id: int
    detection_score: float
    entity_score: float
    bbox_x_min: float
    bbox_y_min: float
    bbox_x_max: float
    bbox_y_max: float


class Detection(DetectionBase):
    """Full Detection schema with ID and UUID for existing detections"""

    id: Optional[int] = None

    @classmethod
    def from_orm(cls, obj: DetectionDAO) -> "Detection":
        return cls(
            id=obj.id,
            uuid=obj.uuid,
            video_id=obj.video_id,
            frame=obj.frame,
            segment_detection_id=obj.segment_detection_id,
            detection_score=obj.detection_score,
            entity_score=obj.entity_score,
            bbox_x_min=obj.bbox_x_min,
            bbox_y_min=obj.bbox_y_min,
            bbox_x_max=obj.bbox_x_max,
            bbox_y_max=obj.bbox_y_max,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class DetectionCreate(DetectionBase):
    """Detection schema for creating new detections without ID"""

    @classmethod
    def to_orm(cls, obj: "DetectionCreate") -> DetectionDAO:
        """Convert to DetectionDAO for database insertion"""
        return DetectionDAO(
            uuid=obj.uuid,
            video_id=obj.video_id,
            frame=obj.frame,
            segment_detection_id=obj.segment_detection_id,
            detection_score=obj.detection_score,
            entity_score=obj.entity_score,
            bbox_x_min=obj.bbox_x_min,
            bbox_y_min=obj.bbox_y_min,
            bbox_x_max=obj.bbox_x_max,
            bbox_y_max=obj.bbox_y_max,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class DetectionUpdate(Timestamps):
    frame: Optional[int] = None
    detection_score: Optional[float] = None
    entity_score: Optional[float] = None
    bbox_x_min: Optional[float] = None
    bbox_y_min: Optional[float] = None
    bbox_x_max: Optional[float] = None
    bbox_y_max: Optional[float] = None
