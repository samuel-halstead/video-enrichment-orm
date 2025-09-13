import uuid
from typing import Optional

from pydantic import Field

from video_enrichment_orm.dao.taxonomy import TaxonomyDAO
from video_enrichment_orm.schemas.timestamps import Timestamps


class TaxonomyBase(Timestamps):
    """Base class for Taxonomy schemas to avoid code duplication"""

    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    label: str
    taxonomy_id: Optional[int] = None


class Taxonomy(TaxonomyBase):
    """Full Taxonomy schema with ID and UUID for existing taxonomies"""

    id: Optional[int] = None

    @classmethod
    def from_orm(cls, obj: TaxonomyDAO) -> "Taxonomy":
        return cls(
            id=obj.id,
            uuid=obj.uuid,
            label=obj.label,
            taxonomy_id=obj.taxonomy_id,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class TaxonomyCreate(TaxonomyBase):
    """Taxonomy schema for creating new taxonomies without ID"""

    @classmethod
    def to_orm(cls, obj: "TaxonomyCreate") -> TaxonomyDAO:
        """Convert to TaxonomyDAO for database insertion"""
        return TaxonomyDAO(
            uuid=obj.uuid,
            label=obj.label,
            taxonomy_id=obj.taxonomy_id,
            created_at=obj.created_at,
            created_by=obj.created_by,
            updated_at=obj.updated_at,
            updated_by=obj.updated_by,
        )


class TaxonomyUpdate(Timestamps):
    label: Optional[str] = None
