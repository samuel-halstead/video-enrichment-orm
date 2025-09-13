import pytest

from video_enrichment_orm.managers.db_taxonomy import db_taxonomy_manager
from video_enrichment_orm.schemas.taxonomy import TaxonomyCreate, TaxonomyUpdate


class TestTaxonomy:
    @classmethod
    def setup_class(cls):
        # run once before any tests in this class
        cls.taxonomy_db_orm_manager = db_taxonomy_manager

    @classmethod
    def teardown_class(cls):
        # run once after all tests in this class
        pass

    @pytest.fixture(autouse=True)
    def cleanup_taxonomies(self):
        # this runs after each test: tear down *any* taxonomies that the test created
        yield
        for t in self.taxonomy_db_orm_manager.get_taxonomies():
            self.taxonomy_db_orm_manager.delete_taxonomy_by_id(t.id)

    def test_insert_and_delete_taxonomy(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        assert taxonomy.id is not None
        assert taxonomy.uuid is not None
        assert taxonomy.label == "test_taxonomy"
        assert taxonomy.taxonomy_id is None

        # Delete taxonomy
        self.taxonomy_db_orm_manager.delete_taxonomy_by_id(taxonomy.id)

        with pytest.raises(ValueError):
            self.taxonomy_db_orm_manager.get_taxonomy_by_id(taxonomy.id)

    def test_update_taxonomy_by_id(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        taxonomy_update = TaxonomyUpdate(
            label="test_taxonomy_updated",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.update_taxonomy(taxonomy_update, id=taxonomy.id)

        assert taxonomy.label == "test_taxonomy_updated"
        assert taxonomy.taxonomy_id is None

    def test_update_taxonomy_by_uuid(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        taxonomy_update = TaxonomyUpdate(
            label="test_taxonomy_updated",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.update_taxonomy(taxonomy_update, uuid=taxonomy.uuid)

        assert taxonomy.label == "test_taxonomy_updated"
        assert taxonomy.taxonomy_id is None

    def test_get_taxonomy_by_id(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        taxonomy_db = self.taxonomy_db_orm_manager.get_taxonomy_by_id(taxonomy.id)
        assert taxonomy_db.label == "test_taxonomy"
        assert taxonomy_db.taxonomy_id is None

    def test_get_taxonomy_by_uuid(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        taxonomy_db = self.taxonomy_db_orm_manager.get_taxonomy_by_uuid(taxonomy.uuid)
        assert taxonomy_db.label == "test_taxonomy"
        assert taxonomy_db.taxonomy_id is None

    def test_get_taxonomy_by_label(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        taxonomy_db = self.taxonomy_db_orm_manager.get_taxonomy_by_label(taxonomy.label)
        assert taxonomy_db.id == taxonomy.id
        assert taxonomy_db.uuid == taxonomy.uuid

    def test_get_taxonomies_by_ids(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        taxonomies_db = self.taxonomy_db_orm_manager.get_taxonomies_by_ids([taxonomy.id])
        assert len(taxonomies_db) == 1
        assert taxonomies_db[0].label == "test_taxonomy"
        assert taxonomies_db[0].taxonomy_id is None

    def test_get_taxonomies_by_uuids(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        taxonomies_db = self.taxonomy_db_orm_manager.get_taxonomies_by_uuids([taxonomy.uuid])
        assert len(taxonomies_db) == 1
        assert taxonomies_db[0].label == "test_taxonomy"
        assert taxonomies_db[0].taxonomy_id is None

    def test_get_taxonomies_by_parent_id(self) -> None:
        # Create a parent taxonomy
        parent_taxonomy = TaxonomyCreate(
            label="test_taxonomy_parent",
            taxonomy_id=None,
        )
        parent_taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(parent_taxonomy)

        # Create a child taxonomy
        child_taxonomy = TaxonomyCreate(
            label="test_taxonomy_child",
            taxonomy_id=parent_taxonomy.id,
        )
        child_taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(child_taxonomy)

        # Test getting children by parent id
        children = self.taxonomy_db_orm_manager.get_taxonomies_by_parent_id(parent_taxonomy.id)
        assert len(children) == 1
        assert children[0].label == "test_taxonomy_child"
        assert children[0].taxonomy_id == parent_taxonomy.id

    def test_delete_taxonomy_by_uuid(self) -> None:
        taxonomy = TaxonomyCreate(
            label="test_taxonomy",
            taxonomy_id=None,
        )
        taxonomy = self.taxonomy_db_orm_manager.save_taxonomy(taxonomy)

        self.taxonomy_db_orm_manager.delete_taxonomy_by_uuid(taxonomy.uuid)

        with pytest.raises(ValueError):
            self.taxonomy_db_orm_manager.get_taxonomy_by_uuid(taxonomy.uuid)
