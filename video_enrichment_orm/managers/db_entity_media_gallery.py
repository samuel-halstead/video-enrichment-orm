from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError

from video_enrichment_orm.core.config import logging
from video_enrichment_orm.core.session_factory import session_scope
from video_enrichment_orm.dao.entity_media_gallery import EntityMediaGalleryDAO
from video_enrichment_orm.exceptions.integrity_exception import IntegrityExceptionError
from video_enrichment_orm.schemas.entity_media_gallery import (
    EntityMediaGallery,
    EntityMediaGalleryCreate,
    EntityMediaGalleryUpdate,
)

logger = logging.getLogger(__name__)


class EntityMediaGalleryDBORMManager:
    @staticmethod
    def get_entity_media_galleries() -> list[EntityMediaGallery]:
        with session_scope() as session:
            media_galleries_orm = session.query(EntityMediaGalleryDAO).all()
            media_galleries = [
                EntityMediaGallery.from_orm(media_gallery_orm) for media_gallery_orm in media_galleries_orm
            ]
        return media_galleries

    @staticmethod
    def get_entity_media_galleries_by_ids(media_gallery_ids: list[int]) -> list[EntityMediaGallery]:
        with session_scope() as session:
            try:
                media_galleries_orm = (
                    session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.id.in_(media_gallery_ids)).all()
                )
                media_galleries = [
                    EntityMediaGallery.from_orm(media_gallery_orm) for media_gallery_orm in media_galleries_orm
                ]
            except Exception as e:
                raise e

        return media_galleries

    @staticmethod
    def get_entity_media_gallery_by_id(media_gallery_id: int) -> EntityMediaGallery:
        with session_scope() as session:
            try:
                media_gallery_orm = (
                    session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.id == media_gallery_id).first()
                )
                media_gallery = EntityMediaGallery.from_orm(media_gallery_orm)
            except Exception as e:
                raise ValueError(f"EntityMediaGallery with id {media_gallery_id} not found") from e

        return media_gallery

    @staticmethod
    def get_entity_media_galleries_by_uuids(media_gallery_uuids: list[str]) -> list[EntityMediaGallery]:
        with session_scope() as session:
            try:
                media_galleries_orm = (
                    session.query(EntityMediaGalleryDAO)
                    .filter(EntityMediaGalleryDAO.uuid.in_(media_gallery_uuids))
                    .all()
                )
                media_galleries = [
                    EntityMediaGallery.from_orm(media_gallery_orm) for media_gallery_orm in media_galleries_orm
                ]
            except Exception as e:
                raise e

        return media_galleries

    @staticmethod
    def get_entity_media_gallery_by_uuid(media_gallery_uuid: str) -> EntityMediaGallery:
        with session_scope() as session:
            media_gallery_orm = (
                session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.uuid == media_gallery_uuid).first()
            )
            if not media_gallery_orm:
                raise ValueError(f"EntityMediaGallery with uuid {media_gallery_uuid} not found")
            media_gallery = EntityMediaGallery.from_orm(media_gallery_orm)
        return media_gallery

    @staticmethod
    def get_entity_media_galleries_by_entity_id(entity_id: int) -> list[EntityMediaGallery]:
        with session_scope() as session:
            media_galleries_orm = (
                session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.entity_id == entity_id).all()
            )
            media_galleries = [
                EntityMediaGallery.from_orm(media_gallery_orm) for media_gallery_orm in media_galleries_orm
            ]
        return media_galleries

    @staticmethod
    def get_enabled_entity_media_galleries_by_entity_id(entity_id: int) -> list[EntityMediaGallery]:
        with session_scope() as session:
            media_galleries_orm = (
                session.query(EntityMediaGalleryDAO)
                .filter(EntityMediaGalleryDAO.enabled, EntityMediaGalleryDAO.entity_id == entity_id)
                .all()
            )
            media_galleries = [
                EntityMediaGallery.from_orm(media_gallery_orm) for media_gallery_orm in media_galleries_orm
            ]
        return media_galleries

    @staticmethod
    def get_enabled_entity_media_galleries() -> list[EntityMediaGallery]:
        with session_scope() as session:
            media_galleries_orm = session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.enabled).all()
            media_galleries = [
                EntityMediaGallery.from_orm(media_gallery_orm) for media_gallery_orm in media_galleries_orm
            ]
        return media_galleries

    def save_entity_media_gallery(self, media_gallery: EntityMediaGalleryCreate) -> EntityMediaGallery:
        media_gallery_orm = EntityMediaGalleryCreate.to_orm(media_gallery)
        return self._save_entity_media_gallery(media_gallery_orm)

    @staticmethod
    def _save_entity_media_gallery(media_gallery_orm: EntityMediaGalleryDAO) -> EntityMediaGallery:
        with session_scope() as session:
            try:
                session.add(media_gallery_orm)
                session.flush()
                return EntityMediaGallery.from_orm(media_gallery_orm)

            except IntegrityError as error:
                logger.debug(f" Error Inserting data into PostgresSQL: {error}")
                raise IntegrityExceptionError(error) from error

    @staticmethod
    def delete_entity_media_gallery_by_id(media_gallery_id: int) -> None:
        with session_scope() as session:
            session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.id == media_gallery_id).delete()

    @staticmethod
    def delete_entity_media_gallery_by_uuid(media_gallery_uuid: str) -> None:
        with session_scope() as session:
            session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.uuid == media_gallery_uuid).delete()

    @staticmethod
    def delete_entity_media_galleries_by_entity_id(entity_id: int) -> None:
        with session_scope() as session:
            session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.entity_id == entity_id).delete()

    @staticmethod
    def soft_delete_entity_media_gallery_by_uuid(media_gallery_uuid: str) -> None:
        """Soft delete by setting enabled to False"""
        with session_scope() as session:
            try:
                media_gallery_orm: EntityMediaGalleryDAO = (
                    session.query(EntityMediaGalleryDAO)
                    .filter(EntityMediaGalleryDAO.uuid == media_gallery_uuid)
                    .first()
                )
                if media_gallery_orm:
                    media_gallery_orm.enabled = False
                    media_gallery_orm.updated_at = datetime.now(timezone.utc)
                    media_gallery_orm.updated_by = "system"
                    session.flush()

            except IntegrityError as error:
                logger.debug(f" Error Soft Deleting data into PostgresSQL: {error}")
                raise IntegrityExceptionError(error) from error

    @staticmethod
    def update_entity_media_gallery(
        media_gallery_update: EntityMediaGalleryUpdate, id: Optional[int] = None, uuid: Optional[str] = None
    ) -> EntityMediaGallery:
        if id is None and uuid is None:
            raise ValueError("Either id or uuid must be provided")
        if id is not None and uuid is not None:
            raise ValueError("Only one of id or uuid must be provided")

        with session_scope() as session:
            if id is not None:
                media_gallery_orm: EntityMediaGalleryDAO = (
                    session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.id == id).first()
                )
            else:
                media_gallery_orm: EntityMediaGalleryDAO = (
                    session.query(EntityMediaGalleryDAO).filter(EntityMediaGalleryDAO.uuid == uuid).first()
                )
            if not media_gallery_orm:
                raise ValueError(f"EntityMediaGallery with {'id' if id else 'uuid'} {id or uuid} not found")

            # Update fields
            for key, value in media_gallery_update.model_dump().items():
                if value is not None:
                    setattr(media_gallery_orm, key, value)

            media_gallery_orm.updated_at = datetime.now(timezone.utc)
            media_gallery_orm.updated_by = "system"

            session.commit()

            # Reload updated object so fields are fresh
            session.refresh(media_gallery_orm)

            # Build the Pydantic model inside the session
            updated_media_gallery = EntityMediaGallery.from_orm(media_gallery_orm)

        return updated_media_gallery


db_entity_media_gallery_manager = EntityMediaGalleryDBORMManager()
