from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from video_enrichment_orm.dao.table_with_timestamps import TableWithTimeStamps


class TaxonomyDAO(TableWithTimeStamps):
    __tablename__ = "taxonomy"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(40), nullable=False, index=True)
    label = Column(String(512), nullable=False)

    taxonomy_id = Column(Integer, ForeignKey("taxonomy.id", ondelete="CASCADE"), nullable=True, index=True)

    __table_args__ = (UniqueConstraint("label"),)
