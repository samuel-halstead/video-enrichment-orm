from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError

from video_enrichment_orm.core.config import logging
from video_enrichment_orm.core.session_factory import session_scope
from video_enrichment_orm.dao import VideoDAO
from video_enrichment_orm.exceptions.integrity_exception import IntegrityExceptionError
from video_enrichment_orm.schemas.video import Video, VideoCreate, VideoUpdate

logger = logging.getLogger(__name__)


class VideoDBORMManager:
    @staticmethod
    def get_videos() -> list[Video]:
        with session_scope() as session:
            try:
                videos_orm = session.query(VideoDAO).all()
                videos = [Video.from_orm(video_orm) for video_orm in videos_orm]
            except Exception as e:
                raise e
        return videos

    @staticmethod
    def get_videos_by_ids(video_ids: list[int]) -> list[Video]:
        with session_scope() as session:
            try:
                videos_orm = session.query(VideoDAO).filter(VideoDAO.id.in_(video_ids)).all()
                videos = [Video.from_orm(video_orm) for video_orm in videos_orm]
            except Exception as e:
                raise e

        return videos

    @staticmethod
    def get_video_by_id(video_id: int) -> Video:
        with session_scope() as session:
            try:
                video_orm = session.query(VideoDAO).filter(VideoDAO.id == video_id).first()
                video = Video.from_orm(video_orm)
            except Exception as e:
                raise ValueError(f"Video with id {video_id} not found") from e

        return video

    @staticmethod
    def get_videos_by_uuids(video_uuids: list[str]) -> list[Video]:
        with session_scope() as session:
            try:
                videos_orm = session.query(VideoDAO).filter(VideoDAO.uuid.in_(video_uuids)).all()
                videos = [Video.from_orm(video_orm) for video_orm in videos_orm]
            except Exception as e:
                raise e
        return videos

    @staticmethod
    def get_video_by_uuid(video_uuid: str) -> Video:
        with session_scope() as session:
            try:
                video_orm = session.query(VideoDAO).filter(VideoDAO.uuid == video_uuid).first()
                video = Video.from_orm(video_orm)
            except Exception as e:
                raise ValueError(f"Video with uuid {video_uuid} not found") from e

        return video

    def save_video(self, video: VideoCreate) -> Video:
        video_orm = VideoCreate.to_orm(video)
        return self._save_video(video_orm)

    @staticmethod
    def _save_video(video_orm: VideoDAO) -> Video:
        with session_scope() as session:
            try:
                session.add(video_orm)
                session.flush()
                return Video.from_orm(video_orm)

            except IntegrityError as error:
                logger.debug(f" Error Inserting data into PostgresSQL: {error}")
                raise IntegrityExceptionError(error) from error

    @staticmethod
    def delete_video_by_id(video_id: int) -> None:
        with session_scope() as session:
            session.query(VideoDAO).filter(VideoDAO.id == video_id).delete()

    @staticmethod
    def delete_video_by_uuid(video_uuid: str) -> None:
        with session_scope() as session:
            session.query(VideoDAO).filter(VideoDAO.uuid == video_uuid).delete()

    @staticmethod
    def update_video(video_update: VideoUpdate, id: Optional[int] = None, uuid: Optional[str] = None) -> Video:
        if id is None and uuid is None:
            raise ValueError("Either id or uuid must be provided")
        if id is not None and uuid is not None:
            raise ValueError("Only one of id or uuid must be provided")

        with session_scope() as session:
            if id is not None:
                video_orm: VideoDAO = session.query(VideoDAO).filter(VideoDAO.id == id).first()
            else:
                video_orm: VideoDAO = session.query(VideoDAO).filter(VideoDAO.uuid == uuid).first()
            if not video_orm:
                raise ValueError(f"Video with {'id' if id else 'uuid'} {video_update.id} not found")

            # Update fields
            for key, value in video_update.model_dump().items():
                if value is not None:
                    setattr(video_orm, key, value)

            video_orm.updated_at = datetime.now(timezone.utc)
            video_orm.updated_by = "system"

            session.commit()

            # Reload updated object so fields are fresh
            session.refresh(video_orm)

            # Build the Pydantic model inside the session
            updated_video = Video.from_orm(video_orm)

        return updated_video


db_video_manager = VideoDBORMManager()
