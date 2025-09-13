import uuid
from typing import Optional

import numpy as np
from pydantic import ConfigDict, Field

from video_enrichment_orm.dao.entity_media_gallery import EntityMediaGalleryDAO
from video_enrichment_orm.schemas.timestamps import Timestamps


class EntityMediaGalleryBase(Timestamps):
    """Base class for EntityMediaGallery schemas to avoid code duplication"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: int
    path: str
    embedding: Optional[np.ndarray] = None
    enabled: Optional[bool] = None


class EntityMediaGallery(EntityMediaGalleryBase):
    """Full EntityMediaGallery schema with ID and UUID for existing entity media galleries"""

    id: Optional[int] = None

    @classmethod
    def from_orm(cls, obj: EntityMediaGalleryDAO) -> "EntityMediaGallery":
        return cls(
            id=obj.id,
            uuid=obj.uuid,
            entity_id=obj.entity_id,
            path=obj.path,
            embedding=np.frombuffer(obj.embedding, dtype=np.float32) if obj.embedding else None,
            enabled=obj.enabled,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class EntityMediaGalleryCreate(EntityMediaGalleryBase):
    """EntityMediaGallery schema for creating new entity media galleries without ID"""

    @classmethod
    def to_orm(cls, obj: "EntityMediaGalleryCreate") -> EntityMediaGalleryDAO:
        """Convert to EntityMediaGalleryDAO for database insertion"""
        return EntityMediaGalleryDAO(
            uuid=obj.uuid,
            entity_id=obj.entity_id,
            path=obj.path,
            embedding=obj.embedding.tobytes() if obj.embedding is not None else None,
            enabled=obj.enabled,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class EntityMediaGalleryUpdate(Timestamps):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    path: Optional[str] = None
    embedding: Optional[np.ndarray | bytes] = None
    enabled: Optional[bool] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.embedding is not None and isinstance(self.embedding, np.ndarray):
            self.embedding = self.embedding.tobytes()
