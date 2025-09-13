from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from video_enrichment_orm.dao.base import Base


class TableWithTimeStamps(Base):  # type: ignore
    __abstract__ = True

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    created_by = Column(String(255), nullable=False, server_default="system")
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    updated_by = Column(String(255), nullable=True, onupdate="system")
