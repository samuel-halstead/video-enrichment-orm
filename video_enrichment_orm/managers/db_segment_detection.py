from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError

from video_enrichment_orm.core.batch import batch_items
from video_enrichment_orm.core.config import logging, settings
from video_enrichment_orm.core.session_factory import session_scope
from video_enrichment_orm.dao.segment_detection import SegmentDetectionDAO
from video_enrichment_orm.exceptions.integrity_exception import IntegrityExceptionError
from video_enrichment_orm.schemas.segment_detection import (
    SegmentDetection,
    SegmentDetectionCreate,
    SegmentDetectionUpdate,
)

logger = logging.getLogger(__name__)


class SegmentDetectionDBORMManager:
    @staticmethod
    def get_segment_detections() -> list[SegmentDetection]:
        with session_scope() as session:
            segment_detections_orm = session.query(SegmentDetectionDAO).all()
            segment_detections = [
                SegmentDetection.from_orm(segment_detection_orm) for segment_detection_orm in segment_detections_orm
            ]
        return segment_detections

    @staticmethod
    def get_segment_detections_by_ids(segment_detection_ids: list[int]) -> list[SegmentDetection]:
        with session_scope() as session:
            try:
                segment_detections_orm = (
                    session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.id.in_(segment_detection_ids)).all()
                )
                segment_detections = [
                    SegmentDetection.from_orm(segment_detection_orm)
                    for segment_detection_orm in segment_detections_orm
                ]
            except Exception as e:
                raise e

        return segment_detections

    @staticmethod
    def get_segment_detection_by_id(segment_detection_id: int) -> SegmentDetection:
        with session_scope() as session:
            try:
                segment_detection_orm = (
                    session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.id == segment_detection_id).first()
                )
                segment_detection = SegmentDetection.from_orm(segment_detection_orm)
            except Exception as e:
                raise ValueError(f"SegmentDetection with id {segment_detection_id} not found") from e

        return segment_detection

    @staticmethod
    def get_segment_detections_by_uuids(segment_detection_uuids: list[str]) -> list[SegmentDetection]:
        with session_scope() as session:
            try:
                segment_detections_orm = (
                    session.query(SegmentDetectionDAO)
                    .filter(SegmentDetectionDAO.uuid.in_(segment_detection_uuids))
                    .all()
                )
                segment_detections = [
                    SegmentDetection.from_orm(segment_detection_orm)
                    for segment_detection_orm in segment_detections_orm
                ]
            except Exception as e:
                raise e

        return segment_detections

    @staticmethod
    def get_segment_detection_by_uuid(segment_detection_uuid: str) -> SegmentDetection:
        with session_scope() as session:
            try:
                segment_detection_orm = (
                    session.query(SegmentDetectionDAO)
                    .filter(SegmentDetectionDAO.uuid == segment_detection_uuid)
                    .first()
                )
                segment_detection = SegmentDetection.from_orm(segment_detection_orm)
            except Exception as e:
                raise ValueError(f"SegmentDetection with uuid {segment_detection_uuid} not found") from e

        return segment_detection

    @staticmethod
    def get_segment_detections_by_video_id(video_id: int) -> list[SegmentDetection]:
        with session_scope() as session:
            segment_detections_orm = (
                session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.video_id == video_id).all()
            )
            segment_detections = [
                SegmentDetection.from_orm(segment_detection_orm) for segment_detection_orm in segment_detections_orm
            ]
        return segment_detections

    @staticmethod
    def get_segment_detections_by_taxonomy_id(taxonomy_id: int) -> list[SegmentDetection]:
        with session_scope() as session:
            segment_detections_orm = (
                session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.taxonomy_id == taxonomy_id).all()
            )
            segment_detections = [
                SegmentDetection.from_orm(segment_detection_orm) for segment_detection_orm in segment_detections_orm
            ]
        return segment_detections

    @staticmethod
    def get_segment_detections_by_entity_id(entity_id: int) -> list[SegmentDetection]:
        with session_scope() as session:
            segment_detections_orm = (
                session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.entity_id == entity_id).all()
            )
            segment_detections = [
                SegmentDetection.from_orm(segment_detection_orm) for segment_detection_orm in segment_detections_orm
            ]
        return segment_detections

    @staticmethod
    def get_segment_detections_by_entity_ids(entity_ids: list[int]) -> list[SegmentDetection]:
        with session_scope() as session:
            segment_detections_orm = (
                session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.entity_id.in_(entity_ids)).all()
            )
            segment_detections = [
                SegmentDetection.from_orm(segment_detection_orm) for segment_detection_orm in segment_detections_orm
            ]
        return segment_detections

    @staticmethod
    def get_segment_detections_by_video_and_taxonomy(video_id: int, taxonomy_id: int) -> list[SegmentDetection]:
        with session_scope() as session:
            segment_detections_orm = (
                session.query(SegmentDetectionDAO)
                .filter(SegmentDetectionDAO.video_id == video_id, SegmentDetectionDAO.taxonomy_id == taxonomy_id)
                .all()
            )
            segment_detections = [
                SegmentDetection.from_orm(segment_detection_orm) for segment_detection_orm in segment_detections_orm
            ]
        return segment_detections

    @staticmethod
    def get_segment_detections_by_video_and_entity(video_id: int, entity_id: int) -> list[SegmentDetection]:
        with session_scope() as session:
            segment_detections_orm = (
                session.query(SegmentDetectionDAO)
                .filter(SegmentDetectionDAO.video_id == video_id, SegmentDetectionDAO.entity_id == entity_id)
                .all()
            )
            segment_detections = [
                SegmentDetection.from_orm(segment_detection_orm) for segment_detection_orm in segment_detections_orm
            ]
        return segment_detections

    @staticmethod
    def get_segment_detections_by_frame_range(
        video_id: int, start_frame: int, end_frame: int
    ) -> list[SegmentDetection]:
        with session_scope() as session:
            segment_detections_orm = (
                session.query(SegmentDetectionDAO)
                .filter(
                    SegmentDetectionDAO.video_id == video_id,
                    SegmentDetectionDAO.start_frame >= start_frame,
                    SegmentDetectionDAO.end_frame <= end_frame,
                )
                .all()
            )
            segment_detections = [
                SegmentDetection.from_orm(segment_detection_orm) for segment_detection_orm in segment_detections_orm
            ]
        return segment_detections

    def save_segment_detection(self, segment_detection: SegmentDetectionCreate) -> SegmentDetection:
        segment_detection_orm = SegmentDetectionCreate.to_orm(segment_detection)
        return self._save_segment_detection(segment_detection_orm)

    @staticmethod
    def _save_segment_detection(segment_detection_orm: SegmentDetectionDAO) -> SegmentDetection:
        with session_scope() as session:
            try:
                session.add(segment_detection_orm)
                session.flush()
                session.refresh(segment_detection_orm)
                return SegmentDetection.from_orm(segment_detection_orm)

            except IntegrityError as error:
                logger.debug(f" Error Inserting data into PostgresSQL: {error}")
                raise IntegrityExceptionError(error) from error

    def batch_save_segment_detections(
        self, segment_detections: list[SegmentDetectionCreate], batch_size: int = None
    ) -> list[SegmentDetection]:
        batch_size = batch_size or settings.BATCH_SIZE
        all_saved_segment_detections = []
        for batch in batch_items(segment_detections, batch_size):
            saved_batch = self._batch_save_segment_detections(batch)
            all_saved_segment_detections.extend(saved_batch)
        return all_saved_segment_detections

    @staticmethod
    def _batch_save_segment_detections(segment_detections: list[SegmentDetectionCreate]) -> list[SegmentDetection]:
        with session_scope() as session:
            try:
                segment_detection_orms = [SegmentDetectionCreate.to_orm(sd) for sd in segment_detections]
                session.add_all(segment_detection_orms)
                session.flush()
                return [SegmentDetection.from_orm(sd) for sd in segment_detection_orms]
            except IntegrityError as error:
                logger.debug(f" Error batch inserting segment detections: {error}")
                raise IntegrityExceptionError(error) from error

    @staticmethod
    def delete_segment_detection_by_id(segment_detection_id: int) -> None:
        with session_scope() as session:
            session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.id == segment_detection_id).delete()

    @staticmethod
    def delete_segment_detection_by_uuid(segment_detection_uuid: str) -> None:
        with session_scope() as session:
            session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.uuid == segment_detection_uuid).delete()

    @staticmethod
    def delete_segment_detections_by_video_id(video_id: int) -> None:
        with session_scope() as session:
            session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.video_id == video_id).delete()

    @staticmethod
    def batch_delete_segment_detections_by_video_id(video_id: int, batch_size: int = None) -> None:
        batch_size = batch_size or settings.BATCH_SIZE
        with session_scope() as session:
            # Get all segment detection IDs for this video
            segment_detection_ids = [
                segment_detection.id
                for segment_detection in session.query(SegmentDetectionDAO.id)
                .filter(SegmentDetectionDAO.video_id == video_id)
                .all()
            ]

            # Delete in batches
            for batch_ids in batch_items(segment_detection_ids, batch_size):
                session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.id.in_(batch_ids)).delete(
                    synchronize_session=False
                )
                session.flush()

    @staticmethod
    def update_segment_detection(
        segment_detection_update: SegmentDetectionUpdate, id: Optional[int] = None, uuid: Optional[str] = None
    ) -> SegmentDetection:
        if id is None and uuid is None:
            raise ValueError("Either id or uuid must be provided")
        if id is not None and uuid is not None:
            raise ValueError("Only one of id or uuid must be provided")

        with session_scope() as session:
            if id is not None:
                segment_detection_orm: SegmentDetectionDAO = (
                    session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.id == id).first()
                )
            else:
                segment_detection_orm: SegmentDetectionDAO = (
                    session.query(SegmentDetectionDAO).filter(SegmentDetectionDAO.uuid == uuid).first()
                )
            if not segment_detection_orm:
                raise ValueError(f"SegmentDetection with {'id' if id else 'uuid'} {id or uuid} not found")

            # Update fields
            for key, value in segment_detection_update.model_dump().items():
                if value is not None:
                    setattr(segment_detection_orm, key, value)

            segment_detection_orm.updated_at = datetime.now(timezone.utc)
            segment_detection_orm.updated_by = "system"

            session.commit()

            # Reload updated object so fields are fresh
            session.refresh(segment_detection_orm)

            # Build the Pydantic model inside the session
            updated_segment_detection = SegmentDetection.from_orm(segment_detection_orm)

        return updated_segment_detection


db_segment_detection_manager = SegmentDetectionDBORMManager()
