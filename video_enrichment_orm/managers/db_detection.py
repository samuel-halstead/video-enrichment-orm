from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError

from video_enrichment_orm.core.batch import batch_items
from video_enrichment_orm.core.config import logging, settings
from video_enrichment_orm.core.session_factory import session_scope
from video_enrichment_orm.dao.detection import DetectionDAO
from video_enrichment_orm.exceptions.integrity_exception import IntegrityExceptionError
from video_enrichment_orm.schemas.detection import (
    Detection,
    DetectionCreate,
    DetectionUpdate,
)

logger = logging.getLogger(__name__)


class DetectionDBORMManager:
    @staticmethod
    def get_detections() -> list[Detection]:
        with session_scope() as session:
            detections_orm = session.query(DetectionDAO).all()
            detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
        return detections

    @staticmethod
    def get_detections_by_ids(detection_ids: list[int]) -> list[Detection]:
        with session_scope() as session:
            try:
                detections_orm = session.query(DetectionDAO).filter(DetectionDAO.id.in_(detection_ids)).all()
                detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
            except Exception as e:
                raise e

        return detections

    @staticmethod
    def get_detection_by_id(detection_id: int) -> Detection:
        with session_scope() as session:
            try:
                detection_orm = session.query(DetectionDAO).filter(DetectionDAO.id == detection_id).first()
                detection = Detection.from_orm(detection_orm)
            except Exception as e:
                raise ValueError(f"Detection with id {detection_id} not found") from e
        return detection

    @staticmethod
    def get_detections_by_uuids(detection_uuids: list[str]) -> list[Detection]:
        with session_scope() as session:
            try:
                detections_orm = session.query(DetectionDAO).filter(DetectionDAO.uuid.in_(detection_uuids)).all()
                detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
            except Exception as e:
                raise e

        return detections

    @staticmethod
    def get_detection_by_uuid(detection_uuid: str) -> Detection:
        with session_scope() as session:
            try:
                detection_orm = session.query(DetectionDAO).filter(DetectionDAO.uuid == detection_uuid).first()
                detection = Detection.from_orm(detection_orm)
            except Exception as e:
                raise ValueError(f"Detection with uuid {detection_uuid} not found") from e
        return detection

    @staticmethod
    def get_detections_by_video_id(video_id: int) -> list[Detection]:
        with session_scope() as session:
            detections_orm = session.query(DetectionDAO).filter(DetectionDAO.video_id == video_id).all()
            detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
        return detections

    @staticmethod
    def get_detections_by_segment_detection_id(segment_detection_id: int) -> list[Detection]:
        with session_scope() as session:
            detections_orm = (
                session.query(DetectionDAO).filter(DetectionDAO.segment_detection_id == segment_detection_id).all()
            )
            detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
        return detections

    @staticmethod
    def get_detections_by_frame(video_id: int, frame: int) -> list[Detection]:
        with session_scope() as session:
            detections_orm = (
                session.query(DetectionDAO)
                .filter(DetectionDAO.video_id == video_id, DetectionDAO.frame == frame)
                .all()
            )
            detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
        return detections

    @staticmethod
    def get_detections_by_frame_range(video_id: int, start_frame: int, end_frame: int) -> list[Detection]:
        with session_scope() as session:
            detections_orm = (
                session.query(DetectionDAO)
                .filter(
                    DetectionDAO.video_id == video_id,
                    DetectionDAO.frame >= start_frame,
                    DetectionDAO.frame <= end_frame,
                )
                .all()
            )
            detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
        return detections

    @staticmethod
    def get_detections_by_score_threshold(video_id: int, min_score: float) -> list[Detection]:
        with session_scope() as session:
            detections_orm = (
                session.query(DetectionDAO)
                .filter(DetectionDAO.video_id == video_id, DetectionDAO.detection_score >= min_score)
                .all()
            )
            detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
        return detections

    @staticmethod
    def get_detections_by_entity_score_threshold(video_id: int, min_entity_score: float) -> list[Detection]:
        with session_scope() as session:
            detections_orm = (
                session.query(DetectionDAO)
                .filter(DetectionDAO.video_id == video_id, DetectionDAO.entity_score >= min_entity_score)
                .all()
            )
            detections = [Detection.from_orm(detection_orm) for detection_orm in detections_orm]
        return detections

    def save_detection(self, detection: DetectionCreate) -> Detection:
        detection_orm = DetectionCreate.to_orm(detection)
        return self._save_detection(detection_orm)

    @staticmethod
    def _save_detection(detection_orm: DetectionDAO) -> Detection:
        with session_scope() as session:
            try:
                session.add(detection_orm)
                session.flush()
                return Detection.from_orm(detection_orm)

            except IntegrityError as error:
                logger.debug(f" Error Inserting data into PostgresSQL: {error}")
                raise IntegrityExceptionError(error) from error

    def batch_save_detections(self, detections: list[DetectionCreate], batch_size: int = None) -> list[Detection]:
        batch_size = batch_size or settings.BATCH_SIZE
        all_saved_detections = []
        for batch in batch_items(detections, batch_size):
            saved_batch = self._batch_save_detections(batch)
            all_saved_detections.extend(saved_batch)
        return all_saved_detections

    @staticmethod
    def _batch_save_detections(detections: list[DetectionCreate]) -> list[Detection]:
        with session_scope() as session:
            try:
                detection_orms = [DetectionCreate.to_orm(d) for d in detections]
                session.add_all(detection_orms)
                session.flush()
                return [Detection.from_orm(d) for d in detection_orms]
            except IntegrityError as error:
                logger.debug(f" Error batch inserting detections: {error}")
                raise IntegrityExceptionError(error) from error

    @staticmethod
    def delete_detection_by_id(detection_id: int) -> None:
        with session_scope() as session:
            session.query(DetectionDAO).filter(DetectionDAO.id == detection_id).delete()

    @staticmethod
    def delete_detection_by_uuid(detection_uuid: str) -> None:
        with session_scope() as session:
            session.query(DetectionDAO).filter(DetectionDAO.uuid == detection_uuid).delete()

    @staticmethod
    def delete_detections_by_video_id(video_id: int) -> None:
        with session_scope() as session:
            session.query(DetectionDAO).filter(DetectionDAO.video_id == video_id).delete()

    @staticmethod
    def batch_delete_detections_by_video_id(video_id: int, batch_size: int = None) -> None:
        batch_size = batch_size or settings.BATCH_SIZE
        with session_scope() as session:
            # Get all detection IDs for this video
            detection_ids = [
                detection.id
                for detection in session.query(DetectionDAO.id).filter(DetectionDAO.video_id == video_id).all()
            ]

            # Delete in batches
            for batch_ids in batch_items(detection_ids, batch_size):
                session.query(DetectionDAO).filter(DetectionDAO.id.in_(batch_ids)).delete(synchronize_session=False)
                session.flush()

    @staticmethod
    def delete_detections_by_segment_detection_id(segment_detection_id: int) -> None:
        with session_scope() as session:
            session.query(DetectionDAO).filter(DetectionDAO.segment_detection_id == segment_detection_id).delete()

    @staticmethod
    def batch_delete_detections_by_segment_detection_id(segment_detection_id: int, batch_size: int = None) -> None:
        batch_size = batch_size or settings.BATCH_SIZE
        with session_scope() as session:
            # Get all detection IDs for this segment detection
            detection_ids = [
                detection.id
                for detection in session.query(DetectionDAO.id)
                .filter(DetectionDAO.segment_detection_id == segment_detection_id)
                .all()
            ]

            # Delete in batches
            for batch_ids in batch_items(detection_ids, batch_size):
                session.query(DetectionDAO).filter(DetectionDAO.id.in_(batch_ids)).delete(synchronize_session=False)
                session.flush()

    @staticmethod
    def update_detection(
        detection_update: DetectionUpdate, id: Optional[int] = None, uuid: Optional[str] = None
    ) -> Detection:
        if id is None and uuid is None:
            raise ValueError("Either id or uuid must be provided")
        if id is not None and uuid is not None:
            raise ValueError("Only one of id or uuid must be provided")

        with session_scope() as session:
            if id is not None:
                detection_orm: DetectionDAO = session.query(DetectionDAO).filter(DetectionDAO.id == id).first()
            else:
                detection_orm: DetectionDAO = session.query(DetectionDAO).filter(DetectionDAO.uuid == uuid).first()
            if not detection_orm:
                raise ValueError(f"Detection with {'id' if id else 'uuid'} {id or uuid} not found")

            # Update fields
            for key, value in detection_update.model_dump().items():
                if value is not None:
                    setattr(detection_orm, key, value)

            detection_orm.updated_at = datetime.now(timezone.utc)
            detection_orm.updated_by = "system"

            session.commit()

            # Reload updated object so fields are fresh
            session.refresh(detection_orm)

            # Build the Pydantic model inside the session
            updated_detection = Detection.from_orm(detection_orm)

        return updated_detection


db_detection_manager = DetectionDBORMManager()
