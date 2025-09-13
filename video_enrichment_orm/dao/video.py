import enum

from sqlalchemy import Boolean, Column, Enum, Float, Integer, String, UniqueConstraint

from video_enrichment_orm.dao.table_with_timestamps import TableWithTimeStamps


class VideoStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoDAO(TableWithTimeStamps):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(512), nullable=False)  # Movie name
    uuid = Column(String(40), nullable=False, index=True)
    path = Column(String(512), nullable=False)  # Movie path
    extension = Column(String(6), nullable=False)  # Movie extension
    frames = Column(Integer, nullable=True)  # Movie extension
    length = Column(Integer, nullable=True)  # Movie length in seconds
    frame_rate = Column(Float, nullable=True)  # Movie frame rate
    is_test = Column(Boolean, nullable=False, default=False)

    status = Column(Enum(VideoStatus), nullable=False, default=VideoStatus.PENDING)
    status_message = Column(String(512), nullable=True)

    __table_args__ = (UniqueConstraint("uuid"),)
