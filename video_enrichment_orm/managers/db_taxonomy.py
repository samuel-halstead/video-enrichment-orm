from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError

from video_enrichment_orm.core.config import logging
from video_enrichment_orm.core.session_factory import session_scope
from video_enrichment_orm.dao import TaxonomyDAO
from video_enrichment_orm.exceptions.integrity_exception import IntegrityExceptionError
from video_enrichment_orm.schemas.taxonomy import (
    Taxonomy,
    TaxonomyCreate,
    TaxonomyUpdate,
)

logger = logging.getLogger(__name__)


class TaxonomyDBORMManager:
    @staticmethod
    def get_taxonomies() -> list[Taxonomy]:
        with session_scope() as session:
            taxonomies_orm = session.query(TaxonomyDAO).all()
            taxonomies = [Taxonomy.from_orm(taxonomy_orm) for taxonomy_orm in taxonomies_orm]
        return taxonomies

    @staticmethod
    def get_taxonomies_by_ids(taxonomy_ids: list[int]) -> list[Taxonomy]:
        with session_scope() as session:
            try:
                taxonomies_orm = session.query(TaxonomyDAO).filter(TaxonomyDAO.id.in_(taxonomy_ids)).all()
                taxonomies = [Taxonomy.from_orm(taxonomy_orm) for taxonomy_orm in taxonomies_orm]
            except Exception as e:
                raise e

        return taxonomies

    @staticmethod
    def get_taxonomy_by_id(taxonomy_id: int) -> Taxonomy:
        with session_scope() as session:
            try:
                taxonomy_orm = session.query(TaxonomyDAO).filter(TaxonomyDAO.id == taxonomy_id).first()
                taxonomy = Taxonomy.from_orm(taxonomy_orm)
            except Exception as e:
                raise ValueError(f"Taxonomy with id {taxonomy_id} not found") from e

        return taxonomy

    @staticmethod
    def get_taxonomies_by_uuids(taxonomy_uuids: list[str]) -> list[Taxonomy]:
        with session_scope() as session:
            try:
                taxonomies_orm = session.query(TaxonomyDAO).filter(TaxonomyDAO.uuid.in_(taxonomy_uuids)).all()
                taxonomies = [Taxonomy.from_orm(taxonomy_orm) for taxonomy_orm in taxonomies_orm]
            except Exception as e:
                raise e

        return taxonomies

    @staticmethod
    def get_taxonomy_by_uuid(taxonomy_uuid: str) -> Taxonomy:
        with session_scope() as session:
            try:
                taxonomy_orm = session.query(TaxonomyDAO).filter(TaxonomyDAO.uuid == taxonomy_uuid).first()
                taxonomy = Taxonomy.from_orm(taxonomy_orm)
            except Exception as e:
                raise ValueError(f"Taxonomy with uuid {taxonomy_uuid} not found") from e

        return taxonomy

    @staticmethod
    def get_taxonomy_by_label(label: str) -> Taxonomy:
        with session_scope() as session:
            taxonomy_orm = session.query(TaxonomyDAO).filter(TaxonomyDAO.label == label).first()
            if not taxonomy_orm:
                raise ValueError(f"Taxonomy with label {label} not found")
            taxonomy = Taxonomy.from_orm(taxonomy_orm)
        return taxonomy

    @staticmethod
    def get_taxonomies_by_parent_id(parent_id: int) -> list[Taxonomy]:
        with session_scope() as session:
            taxonomies_orm = session.query(TaxonomyDAO).filter(TaxonomyDAO.taxonomy_id == parent_id).all()
            taxonomies = [Taxonomy.from_orm(taxonomy_orm) for taxonomy_orm in taxonomies_orm]
        return taxonomies

    def save_taxonomy(self, taxonomy: TaxonomyCreate) -> Taxonomy:
        taxonomy_orm = TaxonomyCreate.to_orm(taxonomy)
        return self._save_taxonomy(taxonomy_orm)

    @staticmethod
    def _save_taxonomy(taxonomy_orm: TaxonomyDAO) -> Taxonomy:
        with session_scope() as session:
            try:
                session.add(taxonomy_orm)
                session.flush()
                return Taxonomy.from_orm(taxonomy_orm)

            except IntegrityError as error:
                logger.debug(f" Error Inserting data into PostgresSQL: {error}")
                raise IntegrityExceptionError(error) from error

    @staticmethod
    def delete_taxonomy_by_id(taxonomy_id: int) -> None:
        with session_scope() as session:
            session.query(TaxonomyDAO).filter(TaxonomyDAO.id == taxonomy_id).delete()

    @staticmethod
    def delete_taxonomy_by_uuid(taxonomy_uuid: str) -> None:
        with session_scope() as session:
            session.query(TaxonomyDAO).filter(TaxonomyDAO.uuid == taxonomy_uuid).delete()

    @staticmethod
    def update_taxonomy(
        taxonomy_update: TaxonomyUpdate, id: Optional[int] = None, uuid: Optional[str] = None
    ) -> Taxonomy:
        if id is None and uuid is None:
            raise ValueError("Either id or uuid must be provided")
        if id is not None and uuid is not None:
            raise ValueError("Only one of id or uuid must be provided")

        with session_scope() as session:
            if id is not None:
                taxonomy_orm: TaxonomyDAO = session.query(TaxonomyDAO).filter(TaxonomyDAO.id == id).first()
            else:
                taxonomy_orm: TaxonomyDAO = session.query(TaxonomyDAO).filter(TaxonomyDAO.uuid == uuid).first()
            if not taxonomy_orm:
                raise ValueError(f"Taxonomy with {'id' if id else 'uuid'} {id or uuid} not found")

            # Update fields
            for key, value in taxonomy_update.model_dump().items():
                if value is not None:
                    setattr(taxonomy_orm, key, value)

            taxonomy_orm.updated_at = datetime.now(timezone.utc)
            taxonomy_orm.updated_by = "system"

            session.commit()

            # Reload updated object so fields are fresh
            session.refresh(taxonomy_orm)

            # Build the Pydantic model inside the session
            updated_taxonomy = Taxonomy.from_orm(taxonomy_orm)

        return updated_taxonomy


db_taxonomy_manager = TaxonomyDBORMManager()
