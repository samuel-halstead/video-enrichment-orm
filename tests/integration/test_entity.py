import pytest

from video_enrichment_orm.managers.db_entity import db_entity_manager
from video_enrichment_orm.managers.db_taxonomy import db_taxonomy_manager
from video_enrichment_orm.schemas.entity import EntityCreate, EntityUpdate
from video_enrichment_orm.schemas.taxonomy import TaxonomyCreate


class TestEntity:
    @classmethod
    def setup_class(cls):
        # run once before any tests in this class
        cls.entity_db_orm_manager = db_entity_manager
        cls.taxonomy_db_orm_manager = db_taxonomy_manager

        # create one taxonomy for *all* tests
        cls.taxonomy = cls.taxonomy_db_orm_manager.save_taxonomy(
            TaxonomyCreate(
                label="test_taxonomy_for_entity",
                taxonomy_id=None,
            )
        )

    @classmethod
    def teardown_class(cls):
        # run once after all tests in this class
        cls.taxonomy_db_orm_manager.delete_taxonomy_by_id(cls.taxonomy.id)

    @pytest.fixture(autouse=True)
    def cleanup_entities(self):
        # this runs after each test: tear down *any* entities that the test created
        yield
        for e in self.entity_db_orm_manager.get_entities_by_taxonomy_id(self.taxonomy.id):
            self.entity_db_orm_manager.delete_entity_by_id(e.id)

    def test_insert_and_delete_entity(self) -> None:
        # First create a taxonomy for the entity
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        assert entity.id is not None
        assert entity.uuid is not None
        assert entity.alias == ["test_alias1", "test_alias2"]
        assert entity.enabled is True
        assert entity.taxonomy_id == self.taxonomy.id

        # Delete entity
        self.entity_db_orm_manager.delete_entity_by_id(entity.id)

        with pytest.raises(ValueError):
            self.entity_db_orm_manager.get_entity_by_id(entity.id)

    def test_update_entity_by_id(self) -> None:
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        entity_update = EntityUpdate(
            alias=["updated_alias1", "updated_alias2"],
            enabled=False,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.update_entity(entity_update, id=entity.id)

        assert entity.alias == ["updated_alias1", "updated_alias2"]
        assert entity.enabled is False
        assert entity.taxonomy_id == self.taxonomy.id

    def test_update_entity_by_uuid(self) -> None:
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        entity_update = EntityUpdate(
            alias=["uuid_updated_alias1", "uuid_updated_alias2"],
            enabled=False,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.update_entity(entity_update, uuid=entity.uuid)

        assert entity.alias == ["uuid_updated_alias1", "uuid_updated_alias2"]
        assert entity.enabled is False
        assert entity.taxonomy_id == self.taxonomy.id

    def test_get_entity_by_id(self) -> None:
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        entity_db = self.entity_db_orm_manager.get_entity_by_id(entity.id)
        assert entity_db.alias == ["test_alias1", "test_alias2"]
        assert entity_db.enabled is True
        assert entity_db.taxonomy_id == self.taxonomy.id

    def test_get_entity_by_uuid(self) -> None:
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        entity_db = self.entity_db_orm_manager.get_entity_by_uuid(entity.uuid)
        assert entity_db.alias == ["test_alias1", "test_alias2"]
        assert entity_db.enabled is True
        assert entity_db.taxonomy_id == self.taxonomy.id

    def test_get_entities_by_ids(self) -> None:
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        entities_db = self.entity_db_orm_manager.get_entities_by_ids([entity.id])
        assert len(entities_db) == 1
        assert entities_db[0].alias == ["test_alias1", "test_alias2"]
        assert entities_db[0].enabled is True
        assert entities_db[0].taxonomy_id == self.taxonomy.id

    def test_get_entities_by_uuids(self) -> None:
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        entities_db = self.entity_db_orm_manager.get_entities_by_uuids([entity.uuid])
        assert len(entities_db) == 1
        assert entities_db[0].alias == ["test_alias1", "test_alias2"]
        assert entities_db[0].enabled is True
        assert entities_db[0].taxonomy_id == self.taxonomy.id

    def test_get_entities_by_taxonomy_id(self) -> None:
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        entities_db = self.entity_db_orm_manager.get_entities_by_taxonomy_id(self.taxonomy.id)
        assert len(entities_db) == 1
        assert entities_db[0].id == entity.id
        assert entities_db[0].taxonomy_id == self.taxonomy.id

    def test_get_enabled_entities_by_taxonomy_id(self) -> None:
        # Create an enabled entity
        enabled_entity = EntityCreate(
            alias=["enabled_entity"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        enabled_entity = self.entity_db_orm_manager.save_entity(enabled_entity)

        # Create a disabled entity
        disabled_entity = EntityCreate(
            alias=["disabled_entity"],
            enabled=False,
            taxonomy_id=self.taxonomy.id,
        )
        disabled_entity = self.entity_db_orm_manager.save_entity(disabled_entity)

        entities = self.entity_db_orm_manager.get_enabled_entities_by_taxonomy_id(self.taxonomy.id)
        assert len(entities) == 1
        assert entities[0].id == enabled_entity.id
        assert entities[0].enabled is True
        assert entities[0].taxonomy_id == self.taxonomy.id

    def test_get_enabled_entities(self) -> None:
        # Create an enabled entity
        enabled_entity = EntityCreate(
            alias=["enabled_entity"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        enabled_entity = self.entity_db_orm_manager.save_entity(enabled_entity)

        # Create a disabled entity
        disabled_entity = EntityCreate(
            alias=["disabled_entity"],
            enabled=False,
            taxonomy_id=self.taxonomy.id,
        )
        disabled_entity = self.entity_db_orm_manager.save_entity(disabled_entity)

        entities = self.entity_db_orm_manager.get_enabled_entities()
        assert len(entities) == 1
        assert entities[0].id == enabled_entity.id
        assert entities[0].enabled is True

    def test_get_entity_by_alias(self) -> None:
        entity = EntityCreate(
            alias=["test_alias1", "test_alias2"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        entity_db = self.entity_db_orm_manager.get_entity_by_alias("test_alias1")
        assert entity_db.id == entity.id
        assert entity_db.uuid == entity.uuid

    def test_soft_delete_entity_by_uuid(self) -> None:
        entity = EntityCreate(
            alias=["soft_delete_test"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        # Soft delete the entity
        self.entity_db_orm_manager.soft_delete_entity_by_uuid(entity.uuid)

        # Verify it's now disabled
        entity_db = self.entity_db_orm_manager.get_entity_by_uuid(entity.uuid)
        assert entity_db.enabled is False

        # Delete entity and taxonomy
        self.entity_db_orm_manager.delete_entity_by_id(entity.id)

    def test_delete_entity_by_uuid(self) -> None:
        entity = EntityCreate(
            alias=["hard_delete_test"],
            enabled=True,
            taxonomy_id=self.taxonomy.id,
        )
        entity = self.entity_db_orm_manager.save_entity(entity)

        self.entity_db_orm_manager.delete_entity_by_uuid(entity.uuid)

        with pytest.raises(ValueError):
            self.entity_db_orm_manager.get_entity_by_uuid(entity.uuid)

        # Delete entity
        self.entity_db_orm_manager.delete_entity_by_id(entity.id)
