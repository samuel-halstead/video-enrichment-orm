from sqlalchemy import Column, Float, ForeignKey, Integer, String

from video_enrichment_orm.dao.table_with_timestamps import TableWithTimeStamps


class DetectionDAO(TableWithTimeStamps):
    __tablename__ = "detection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(40), nullable=False, index=True, unique=True)
    video_id = Column(Integer, ForeignKey("video.id", ondelete="CASCADE"), nullable=False, index=True)
    frame = Column(Integer, nullable=False)

    # In case we have detections without entity_id we want to be able to classify the type of entity detected
    segment_detection_id = Column(
        Integer, ForeignKey("segment_detection.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # 0.0 - 1.0
    detection_score = Column(Float, nullable=False)

    # 0.0 - 1.0
    entity_score = Column(Float, nullable=False)

    # x_min, y_min, x_max, y_max: % 1
    bbox_x_min = Column(Float, nullable=False)
    bbox_y_min = Column(Float, nullable=False)
    bbox_x_max = Column(Float, nullable=False)
    bbox_y_max = Column(Float, nullable=False)
