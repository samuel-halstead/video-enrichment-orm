from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError

from video_enrichment_orm.core.config import logging
from video_enrichment_orm.core.session_factory import session_scope
from video_enrichment_orm.dao.entity import EntityDAO
from video_enrichment_orm.exceptions.integrity_exception import IntegrityExceptionError
from video_enrichment_orm.schemas.entity import Entity, EntityCreate, EntityUpdate

logger = logging.getLogger(__name__)


class EntityDBORMManager:
    @staticmethod
    def get_entities_by_ids(entity_ids: list[int]) -> list[Entity]:
        with session_scope() as session:
            try:
                entities_orm = session.query(EntityDAO).filter(EntityDAO.id.in_(entity_ids)).all()
                entities = [Entity.from_orm(entity_orm) for entity_orm in entities_orm]
            except Exception as e:
                raise e

        return entities

    @staticmethod
    def get_entity_by_id(entity_id: int) -> Entity:
        with session_scope() as session:
            entity_orm = session.query(EntityDAO).filter(EntityDAO.id == entity_id).first()
            if not entity_orm:
                raise ValueError(f"Entity with id {entity_id} not found")
            entity = Entity.from_orm(entity_orm)
        return entity

    @staticmethod
    def get_entities_by_uuids(entity_uuids: list[str]) -> list[Entity]:
        with session_scope() as session:
            try:
                entities_orm = session.query(EntityDAO).filter(EntityDAO.uuid.in_(entity_uuids)).all()
                entities = [Entity.from_orm(entity_orm) for entity_orm in entities_orm]
            except Exception as e:
                raise e

        return entities

    @staticmethod
    def get_entity_by_uuid(entity_uuid: str) -> Entity:
        with session_scope() as session:
            entity_orm = session.query(EntityDAO).filter(EntityDAO.uuid == entity_uuid).first()
            if not entity_orm:
                raise ValueError(f"Entity with uuid {entity_uuid} not found")
            entity = Entity.from_orm(entity_orm)
        return entity

    @staticmethod
    def get_entities_by_taxonomy_id(taxonomy_id: int) -> list[Entity]:
        with session_scope() as session:
            entities_orm = session.query(EntityDAO).filter(EntityDAO.taxonomy_id == taxonomy_id).all()
            entities = [Entity.from_orm(entity_orm) for entity_orm in entities_orm]
        return entities

    @staticmethod
    def get_enabled_entities_by_taxonomy_id(taxonomy_id: int) -> list[Entity]:
        with session_scope() as session:
            entities_orm = (
                session.query(EntityDAO).filter(EntityDAO.enabled, EntityDAO.taxonomy_id == taxonomy_id).all()
            )
            entities = [Entity.from_orm(entity_orm) for entity_orm in entities_orm]
        return entities

    @staticmethod
    def get_enabled_entities() -> list[Entity]:
        with session_scope() as session:
            entities_orm = session.query(EntityDAO).filter(EntityDAO.enabled).all()
            entities = [Entity.from_orm(entity_orm) for entity_orm in entities_orm]
        return entities

    @staticmethod
    def get_entity_by_alias(alias: str) -> Entity:
        with session_scope() as session:
            # Use any() to check if the alias exists in the array
            entity_orm = session.query(EntityDAO).filter(EntityDAO.alias.any(alias)).first()
            if not entity_orm:
                raise ValueError(f"Entity with alias {alias} not found")
            entity = Entity.from_orm(entity_orm)
        return entity

    def save_entity(self, entity: EntityCreate) -> Entity:
        entity_orm = EntityCreate.to_orm(entity)
        return self._save_entity(entity_orm)

    @staticmethod
    def _save_entity(entity_orm: EntityDAO) -> Entity:
        with session_scope() as session:
            try:
                session.add(entity_orm)
                session.flush()
                return Entity.from_orm(entity_orm)

            except IntegrityError as error:
                logger.debug(f" Error Inserting data into PostgresSQL: {error}")
                raise IntegrityExceptionError(error) from error

    @staticmethod
    def delete_entity_by_id(entity_id: int) -> None:
        with session_scope() as session:
            session.query(EntityDAO).filter(EntityDAO.id == entity_id).delete()

    @staticmethod
    def delete_entity_by_uuid(entity_uuid: str) -> None:
        with session_scope() as session:
            session.query(EntityDAO).filter(EntityDAO.uuid == entity_uuid).delete()

    @staticmethod
    def soft_delete_entity_by_uuid(entity_uuid: str) -> None:
        """Soft delete by setting enabled to False"""
        with session_scope() as session:
            try:
                entity_orm: EntityDAO = session.query(EntityDAO).filter(EntityDAO.uuid == entity_uuid).first()
                if entity_orm:
                    entity_orm.enabled = False
                    entity_orm.updated_at = datetime.now(timezone.utc)
                    entity_orm.updated_by = "system"
                    session.flush()

            except IntegrityError as error:
                logger.debug(f" Error Soft Deleting data into PostgresSQL: {error}")
                raise IntegrityExceptionError(error) from error

    @staticmethod
    def update_entity(entity_update: EntityUpdate, id: Optional[int] = None, uuid: Optional[str] = None) -> Entity:
        if id is None and uuid is None:
            raise ValueError("Either id or uuid must be provided")
        if id is not None and uuid is not None:
            raise ValueError("Only one of id or uuid must be provided")

        with session_scope() as session:
            if id is not None:
                entity_orm: EntityDAO = session.query(EntityDAO).filter(EntityDAO.id == id).first()
            else:
                entity_orm: EntityDAO = session.query(EntityDAO).filter(EntityDAO.uuid == uuid).first()
            if not entity_orm:
                raise ValueError(f"Entity with id {id or uuid} not found")

            # Update fields
            for key, value in entity_update.model_dump().items():
                if value is not None:
                    setattr(entity_orm, key, value)

            entity_orm.updated_at = datetime.now(timezone.utc)
            entity_orm.updated_by = "system"

            session.commit()

            # Reload updated object so fields are fresh
            session.refresh(entity_orm)

            # Build the Pydantic model inside the session
            updated_entity = Entity.from_orm(entity_orm)

        return updated_entity


db_entity_manager = EntityDBORMManager()
