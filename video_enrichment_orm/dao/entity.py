from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList

from video_enrichment_orm.dao.table_with_timestamps import TableWithTimeStamps


class EntityDAO(TableWithTimeStamps):
    __tablename__ = "entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(40), nullable=False, index=True, unique=True)
    alias = Column(MutableList.as_mutable(ARRAY(String)), nullable=False, default=list)
    enabled = Column(Boolean, nullable=False, default=False)

    taxonomy_id = Column(Integer, ForeignKey("taxonomy.id", ondelete="CASCADE"), nullable=False, index=True)
