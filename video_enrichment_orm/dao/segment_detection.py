from sqlalchemy import Column, ForeignKey, Integer, String

from video_enrichment_orm.dao.table_with_timestamps import TableWithTimeStamps


class SegmentDetectionDAO(TableWithTimeStamps):
    __tablename__ = "segment_detection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(40), nullable=False, index=True, unique=True)
    video_id = Column(Integer, ForeignKey("video.id", ondelete="CASCADE"), nullable=False, index=True)
    start_frame = Column(Integer, nullable=False)
    end_frame = Column(Integer, nullable=False)

    # The id of the taxonomy that is detected in the segment
    taxonomy_id = Column(Integer, ForeignKey("taxonomy.id", ondelete="CASCADE"), nullable=False, index=True)

    # The id of the entity that is detected in the segment
    entity_id = Column(Integer, ForeignKey("entity.id", ondelete="CASCADE"), nullable=False, index=True)
