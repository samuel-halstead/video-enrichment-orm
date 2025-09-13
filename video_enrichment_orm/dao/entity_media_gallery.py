from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    UniqueConstraint,
)

from video_enrichment_orm.dao.table_with_timestamps import TableWithTimeStamps


class EntityMediaGalleryDAO(TableWithTimeStamps):
    __tablename__ = "entity_media_gallery"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(40), nullable=False, index=True, unique=True)

    entity_id = Column(Integer, ForeignKey("entity.id", ondelete="CASCADE"), nullable=False, index=True)

    path = Column(String(512), nullable=False)
    embedding = Column(LargeBinary, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)

    __table_args__ = (UniqueConstraint("entity_id", "path"),)
