import numpy as np
import pytest

from video_enrichment_orm.managers.db_entity import db_entity_manager
from video_enrichment_orm.managers.db_entity_media_gallery import (
    db_entity_media_gallery_manager,
)
from video_enrichment_orm.managers.db_taxonomy import db_taxonomy_manager
from video_enrichment_orm.schemas.entity import EntityCreate
from video_enrichment_orm.schemas.entity_media_gallery import (
    EntityMediaGalleryCreate,
    EntityMediaGalleryUpdate,
)
from video_enrichment_orm.schemas.taxonomy import TaxonomyCreate


class TestEntityMediaGallery:
    @classmethod
    def setup_class(cls):
        # run once before any tests in this class
        cls.media_gallery_db_orm_manager = db_entity_media_gallery_manager
        cls.entity_db_orm_manager = db_entity_manager
        cls.taxonomy_db_orm_manager = db_taxonomy_manager

        # create one taxonomy and entity for *all* tests
        cls.taxonomy = cls.taxonomy_db_orm_manager.save_taxonomy(
            TaxonomyCreate(
                label="test_taxonomy_for_entity_media_gallery",
                taxonomy_id=None,
            )
        )

        cls.entity = cls.entity_db_orm_manager.save_entity(
            EntityCreate(
                alias=["test_entity_for_media_gallery"],
                enabled=True,
                taxonomy_id=cls.taxonomy.id,
            )
        )

    @classmethod
    def teardown_class(cls):
        # run once after all tests in this class
        cls.entity_db_orm_manager.delete_entity_by_id(cls.entity.id)
        cls.taxonomy_db_orm_manager.delete_taxonomy_by_id(cls.taxonomy.id)

    @pytest.fixture(autouse=True)
    def cleanup_entity_media_galleries(self):
        # this runs after each test: tear down *any* entity media galleries that the test created
        yield
        for mg in self.media_gallery_db_orm_manager.get_entity_media_galleries_by_entity_id(self.entity.id):
            self.media_gallery_db_orm_manager.delete_entity_media_gallery_by_id(mg.id)

    def test_insert_and_delete_entity_media_gallery(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/test/path/to/media.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        assert media_gallery.id is not None
        assert media_gallery.uuid is not None
        assert media_gallery.entity_id == self.entity.id
        assert media_gallery.path == "/test/path/to/media.jpg"
        assert media_gallery.enabled is True
        assert media_gallery.embedding is not None
        assert np.array_equal(media_gallery.embedding, test_embedding)

        # Delete media gallery
        self.media_gallery_db_orm_manager.delete_entity_media_gallery_by_id(media_gallery.id)

        with pytest.raises(ValueError):
            self.media_gallery_db_orm_manager.get_entity_media_gallery_by_id(media_gallery.id)

    def test_update_entity_media_gallery_by_id(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/test/path/to/media.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        # Create new embedding for update
        updated_embedding = np.random.rand(512).astype(np.float32)

        media_gallery_update = EntityMediaGalleryUpdate(
            path="/updated/path/to/media.jpg",
            embedding=updated_embedding,
            enabled=False,
            entity_id=self.entity.id,
        )
        media_gallery = self.media_gallery_db_orm_manager.update_entity_media_gallery(
            media_gallery_update, id=media_gallery.id
        )

        assert media_gallery.path == "/updated/path/to/media.jpg"
        assert media_gallery.enabled is False
        assert media_gallery.entity_id == self.entity.id
        # Check that embedding was updated
        assert media_gallery.embedding is not None
        assert np.array_equal(media_gallery.embedding, updated_embedding)

    def test_update_entity_media_gallery_by_uuid(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/test/path/to/media.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        # Create new embedding for update
        uuid_updated_embedding = np.random.rand(512).astype(np.float32)

        media_gallery_update = EntityMediaGalleryUpdate(
            path="/uuid_updated/path/to/media.jpg",
            embedding=uuid_updated_embedding,
            enabled=True,
            entity_id=self.entity.id,
        )
        media_gallery = self.media_gallery_db_orm_manager.update_entity_media_gallery(
            media_gallery_update, uuid=media_gallery.uuid
        )

        assert media_gallery.path == "/uuid_updated/path/to/media.jpg"
        assert media_gallery.enabled is True
        assert media_gallery.entity_id == self.entity.id
        # Check that embedding was updated
        assert media_gallery.embedding is not None
        assert np.array_equal(media_gallery.embedding, uuid_updated_embedding)

    def test_get_entity_media_gallery_by_id(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/test/path/to/media.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        media_gallery_db = self.media_gallery_db_orm_manager.get_entity_media_gallery_by_id(media_gallery.id)
        assert media_gallery_db.path == "/test/path/to/media.jpg"
        assert media_gallery_db.enabled is True
        assert media_gallery_db.entity_id == self.entity.id
        assert media_gallery_db.embedding is not None
        assert np.array_equal(media_gallery_db.embedding, test_embedding)

    def test_get_entity_media_gallery_by_uuid(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/test/path/to/media.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        media_gallery_db = self.media_gallery_db_orm_manager.get_entity_media_gallery_by_uuid(media_gallery.uuid)
        assert media_gallery_db.path == "/test/path/to/media.jpg"
        assert media_gallery_db.enabled is True
        assert media_gallery_db.entity_id == self.entity.id
        assert media_gallery_db.embedding is not None
        assert np.array_equal(media_gallery_db.embedding, test_embedding)

    def test_get_entity_media_galleries_by_ids(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/test/path/to/media.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        media_galleries_db = self.media_gallery_db_orm_manager.get_entity_media_galleries_by_ids([media_gallery.id])
        assert len(media_galleries_db) == 1
        assert media_galleries_db[0].path == "/test/path/to/media.jpg"
        assert media_galleries_db[0].enabled is True
        assert media_galleries_db[0].entity_id == self.entity.id
        assert media_galleries_db[0].embedding is not None
        assert np.array_equal(media_galleries_db[0].embedding, test_embedding)

    def test_get_entity_media_galleries_by_uuids(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/test/path/to/media.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        media_galleries_db = self.media_gallery_db_orm_manager.get_entity_media_galleries_by_uuids(
            [media_gallery.uuid]
        )
        assert len(media_galleries_db) == 1
        assert media_galleries_db[0].path == "/test/path/to/media.jpg"
        assert media_galleries_db[0].enabled is True
        assert media_galleries_db[0].entity_id == self.entity.id
        assert media_galleries_db[0].embedding is not None
        assert np.array_equal(media_galleries_db[0].embedding, test_embedding)

    def test_get_entity_media_galleries_by_entity_id(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/test/path/to/media.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        media_galleries_db = self.media_gallery_db_orm_manager.get_entity_media_galleries_by_entity_id(self.entity.id)
        assert len(media_galleries_db) == 1
        assert media_galleries_db[0].id == media_gallery.id
        assert media_galleries_db[0].entity_id == self.entity.id

    def test_get_enabled_entity_media_galleries_by_entity_id(self) -> None:
        # Create an enabled media gallery
        enabled_embedding = np.random.rand(512).astype(np.float32)
        enabled_media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/enabled/media.jpg",
            embedding=enabled_embedding,
            enabled=True,
        )
        enabled_media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(enabled_media_gallery)

        # Create a disabled media gallery
        disabled_embedding = np.random.rand(512).astype(np.float32)
        disabled_media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/disabled/media.jpg",
            embedding=disabled_embedding,
            enabled=False,
        )
        disabled_media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(disabled_media_gallery)

        media_galleries = self.media_gallery_db_orm_manager.get_enabled_entity_media_galleries_by_entity_id(
            self.entity.id
        )
        assert len(media_galleries) == 1
        assert media_galleries[0].id == enabled_media_gallery.id
        assert media_galleries[0].enabled is True
        assert media_galleries[0].entity_id == self.entity.id

    def test_get_enabled_entity_media_galleries(self) -> None:
        # Create an enabled media gallery
        enabled_embedding = np.random.rand(512).astype(np.float32)
        enabled_media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/enabled/media.jpg",
            embedding=enabled_embedding,
            enabled=True,
        )
        enabled_media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(enabled_media_gallery)

        # Create a disabled media gallery
        disabled_embedding = np.random.rand(512).astype(np.float32)
        disabled_media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/disabled/media.jpg",
            embedding=disabled_embedding,
            enabled=False,
        )
        disabled_media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(disabled_media_gallery)

        media_galleries = self.media_gallery_db_orm_manager.get_enabled_entity_media_galleries()
        assert len(media_galleries) == 1
        assert media_galleries[0].id == enabled_media_gallery.id
        assert media_galleries[0].enabled is True

    def test_soft_delete_entity_media_gallery_by_uuid(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/soft_delete_test.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        # Soft delete the media gallery
        self.media_gallery_db_orm_manager.soft_delete_entity_media_gallery_by_uuid(media_gallery.uuid)

        # Verify it's now disabled
        media_gallery_db = self.media_gallery_db_orm_manager.get_entity_media_gallery_by_uuid(media_gallery.uuid)
        assert media_gallery_db.enabled is False

    def test_delete_entity_media_gallery_by_uuid(self) -> None:
        # Create test embedding
        test_embedding = np.random.rand(512).astype(np.float32)

        media_gallery = EntityMediaGalleryCreate(
            entity_id=self.entity.id,
            path="/hard_delete_test.jpg",
            embedding=test_embedding,
            enabled=True,
        )
        media_gallery = self.media_gallery_db_orm_manager.save_entity_media_gallery(media_gallery)

        self.media_gallery_db_orm_manager.delete_entity_media_gallery_by_uuid(media_gallery.uuid)

        with pytest.raises(ValueError):
            self.media_gallery_db_orm_manager.get_entity_media_gallery_by_uuid(media_gallery.uuid)
