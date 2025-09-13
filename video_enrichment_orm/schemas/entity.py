import uuid
from typing import Optional

from pydantic import Field

from video_enrichment_orm.dao.entity import EntityDAO
from video_enrichment_orm.schemas.timestamps import Timestamps


class EntityBase(Timestamps):
    """Base class for Entity schemas to avoid code duplication"""

    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    alias: list[str]
    enabled: Optional[bool] = Field(default=True)
    taxonomy_id: int


class Entity(EntityBase):
    """Full Entity schema with ID and UUID for existing entities"""

    id: Optional[int] = None

    @classmethod
    def from_orm(cls, obj: EntityDAO) -> "Entity":
        return cls(
            id=obj.id,
            uuid=obj.uuid,
            alias=obj.alias,
            enabled=obj.enabled,
            taxonomy_id=obj.taxonomy_id,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class EntityCreate(EntityBase):
    """Entity schema for creating new entities without ID"""

    @classmethod
    def to_orm(cls, obj: "EntityCreate") -> EntityDAO:
        """Convert to EntityDAO for database insertion"""
        return EntityDAO(
            uuid=obj.uuid,
            alias=obj.alias,
            enabled=obj.enabled,
            taxonomy_id=obj.taxonomy_id,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class EntityUpdate(Timestamps):
    alias: Optional[list[str]] = None
    enabled: Optional[bool] = None
