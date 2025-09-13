import pytest

from video_enrichment_orm.managers.db_entity import db_entity_manager
from video_enrichment_orm.managers.db_segment_detection import (
    db_segment_detection_manager,
)
from video_enrichment_orm.managers.db_taxonomy import db_taxonomy_manager
from video_enrichment_orm.managers.db_video import db_video_manager
from video_enrichment_orm.schemas.entity import EntityCreate
from video_enrichment_orm.schemas.segment_detection import (
    SegmentDetectionCreate,
    SegmentDetectionUpdate,
)
from video_enrichment_orm.schemas.taxonomy import TaxonomyCreate
from video_enrichment_orm.schemas.video import VideoCreate


class TestSegmentDetection:
    @classmethod
    def setup_class(cls):
        # run once before any tests in this class
        cls.segment_detection_db_orm_manager = db_segment_detection_manager
        cls.video_db_orm_manager = db_video_manager
        cls.taxonomy_db_orm_manager = db_taxonomy_manager
        cls.entity_db_orm_manager = db_entity_manager

        # create one video, taxonomy, and entity for *all* tests
        cls.video = cls.video_db_orm_manager.save_video(
            VideoCreate(
                code="test_video_for_segment_detection",
                path="/test/path/to/video.mp4",
                extension="mp4",
            )
        )

        cls.taxonomy = cls.taxonomy_db_orm_manager.save_taxonomy(
            TaxonomyCreate(
                label="test_taxonomy_for_segment_detection",
                taxonomy_id=None,
            )
        )

        cls.entity = cls.entity_db_orm_manager.save_entity(
            EntityCreate(
                alias=["test_entity_for_segment_detection"],
                enabled=True,
                taxonomy_id=cls.taxonomy.id,
            )
        )

    @classmethod
    def teardown_class(cls):
        # run once after all tests in this class
        cls.entity_db_orm_manager.delete_entity_by_id(cls.entity.id)
        cls.taxonomy_db_orm_manager.delete_taxonomy_by_id(cls.taxonomy.id)
        cls.video_db_orm_manager.delete_video_by_id(cls.video.id)

    @pytest.fixture(autouse=True)
    def cleanup_segment_detections(self):
        # this runs after each test: tear down *any* segment detections that the test created
        yield
        for sd in self.segment_detection_db_orm_manager.get_segment_detections_by_video_id(self.video.id):
            self.segment_detection_db_orm_manager.delete_segment_detection_by_id(sd.id)

    def test_insert_and_delete_segment_detection(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        assert segment_detection.id is not None
        assert segment_detection.uuid is not None
        assert segment_detection.video_id == self.video.id
        assert segment_detection.start_frame == 100
        assert segment_detection.end_frame == 200
        assert segment_detection.taxonomy_id == self.taxonomy.id
        assert segment_detection.entity_id == self.entity.id

        # Delete segment detection
        self.segment_detection_db_orm_manager.delete_segment_detection_by_id(segment_detection.id)

        with pytest.raises(ValueError):
            self.segment_detection_db_orm_manager.get_segment_detection_by_id(segment_detection.id)

    def test_update_segment_detection_by_id(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Update segment detection
        segment_detection_update = SegmentDetectionUpdate(
            start_frame=150,
            end_frame=250,
        )
        segment_detection = self.segment_detection_db_orm_manager.update_segment_detection(
            segment_detection_update, id=segment_detection.id
        )

        assert segment_detection.start_frame == 150
        assert segment_detection.end_frame == 250
        assert segment_detection.video_id == self.video.id
        assert segment_detection.taxonomy_id == self.taxonomy.id
        assert segment_detection.entity_id == self.entity.id

    def test_update_segment_detection_by_uuid(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Update segment detection
        segment_detection_update = SegmentDetectionUpdate(
            start_frame=200,
            end_frame=300,
        )
        segment_detection = self.segment_detection_db_orm_manager.update_segment_detection(
            segment_detection_update, uuid=segment_detection.uuid
        )

        assert segment_detection.start_frame == 200
        assert segment_detection.end_frame == 300
        assert segment_detection.video_id == self.video.id
        assert segment_detection.taxonomy_id == self.taxonomy.id
        assert segment_detection.entity_id == self.entity.id

    def test_get_segment_detection_by_id(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detection by ID
        segment_detection_db = self.segment_detection_db_orm_manager.get_segment_detection_by_id(segment_detection.id)
        assert segment_detection_db.video_id == self.video.id
        assert segment_detection_db.start_frame == 100
        assert segment_detection_db.end_frame == 200
        assert segment_detection_db.taxonomy_id == self.taxonomy.id
        assert segment_detection_db.entity_id == self.entity.id

    def test_get_segment_detection_by_uuid(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detection by UUID
        segment_detection_db = self.segment_detection_db_orm_manager.get_segment_detection_by_uuid(
            segment_detection.uuid
        )
        assert segment_detection_db.video_id == self.video.id
        assert segment_detection_db.start_frame == 100
        assert segment_detection_db.end_frame == 200
        assert segment_detection_db.taxonomy_id == self.taxonomy.id
        assert segment_detection_db.entity_id == self.entity.id

    def test_get_segment_detections_by_ids(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detections by IDs
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_ids(
            [segment_detection.id]
        )
        assert len(segment_detections_db) == 1
        assert segment_detections_db[0].video_id == self.video.id
        assert segment_detections_db[0].start_frame == 100
        assert segment_detections_db[0].end_frame == 200
        assert segment_detections_db[0].taxonomy_id == self.taxonomy.id
        assert segment_detections_db[0].entity_id == self.entity.id

    def test_get_segment_detections_by_uuids(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detections by UUIDs
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_uuids(
            [segment_detection.uuid]
        )
        assert len(segment_detections_db) == 1
        assert segment_detections_db[0].video_id == self.video.id
        assert segment_detections_db[0].start_frame == 100
        assert segment_detections_db[0].end_frame == 200
        assert segment_detections_db[0].taxonomy_id == self.taxonomy.id
        assert segment_detections_db[0].entity_id == self.entity.id

    def test_get_segment_detections_by_video_id(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detections by video ID
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_video_id(self.video.id)
        assert len(segment_detections_db) == 1
        assert segment_detections_db[0].id == segment_detection.id
        assert segment_detections_db[0].video_id == self.video.id

    def test_get_segment_detections_by_taxonomy_id(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detections by taxonomy ID
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_taxonomy_id(
            self.taxonomy.id
        )
        assert len(segment_detections_db) == 1
        assert segment_detections_db[0].id == segment_detection.id
        assert segment_detections_db[0].taxonomy_id == self.taxonomy.id

    def test_get_segment_detections_by_entity_id(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detections by entity ID
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_entity_id(
            self.entity.id
        )
        assert len(segment_detections_db) == 1
        assert segment_detections_db[0].id == segment_detection.id
        assert segment_detections_db[0].entity_id == self.entity.id

    def test_get_segment_detections_by_video_and_taxonomy(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detections by video and taxonomy
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_video_and_taxonomy(
            self.video.id, self.taxonomy.id
        )
        assert len(segment_detections_db) == 1
        assert segment_detections_db[0].id == segment_detection.id
        assert segment_detections_db[0].video_id == self.video.id
        assert segment_detections_db[0].taxonomy_id == self.taxonomy.id

    def test_get_segment_detections_by_video_and_entity(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detections by video and entity
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_video_and_entity(
            self.video.id, self.entity.id
        )
        assert len(segment_detections_db) == 1
        assert segment_detections_db[0].id == segment_detection.id
        assert segment_detections_db[0].video_id == self.video.id
        assert segment_detections_db[0].entity_id == self.entity.id

    def test_get_segment_detections_by_frame_range(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Get segment detections by frame range
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_frame_range(
            self.video.id, 50, 250
        )
        assert len(segment_detections_db) == 1
        assert segment_detections_db[0].id == segment_detection.id
        assert segment_detections_db[0].start_frame == 100
        assert segment_detections_db[0].end_frame == 200

    def test_delete_segment_detection_by_uuid(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Delete segment detection by UUID
        self.segment_detection_db_orm_manager.delete_segment_detection_by_uuid(segment_detection.uuid)

        with pytest.raises(ValueError):
            self.segment_detection_db_orm_manager.get_segment_detection_by_uuid(segment_detection.uuid)

    def test_delete_segment_detections_by_video_id(self) -> None:
        # Create segment detection
        segment_detection = SegmentDetectionCreate(
            video_id=self.video.id,
            start_frame=100,
            end_frame=200,
            taxonomy_id=self.taxonomy.id,
            entity_id=self.entity.id,
        )
        segment_detection = self.segment_detection_db_orm_manager.save_segment_detection(segment_detection)

        # Delete segment detections by video ID
        self.segment_detection_db_orm_manager.delete_segment_detections_by_video_id(self.video.id)

        # Verify it's deleted
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_video_id(self.video.id)
        assert len(segment_detections_db) == 0

    def test_batch_save_segment_detections(self) -> None:
        # Create multiple segment detections
        segment_detections = [
            SegmentDetectionCreate(
                video_id=self.video.id,
                start_frame=100,
                end_frame=200,
                taxonomy_id=self.taxonomy.id,
                entity_id=self.entity.id,
            ),
            SegmentDetectionCreate(
                video_id=self.video.id,
                start_frame=300,
                end_frame=400,
                taxonomy_id=self.taxonomy.id,
                entity_id=self.entity.id,
            ),
        ]

        # Batch save segment detections
        saved_segment_detections = self.segment_detection_db_orm_manager.batch_save_segment_detections(
            segment_detections
        )

        assert len(saved_segment_detections) == 2
        assert saved_segment_detections[0].video_id == self.video.id
        assert saved_segment_detections[0].start_frame == 100
        assert saved_segment_detections[0].end_frame == 200
        assert saved_segment_detections[1].video_id == self.video.id
        assert saved_segment_detections[1].start_frame == 300
        assert saved_segment_detections[1].end_frame == 400

    def test_batch_delete_segment_detections_by_video_id(self) -> None:
        # Create multiple segment detections
        segment_detections = [
            SegmentDetectionCreate(
                video_id=self.video.id,
                start_frame=100,
                end_frame=200,
                taxonomy_id=self.taxonomy.id,
                entity_id=self.entity.id,
            ),
            SegmentDetectionCreate(
                video_id=self.video.id,
                start_frame=300,
                end_frame=400,
                taxonomy_id=self.taxonomy.id,
                entity_id=self.entity.id,
            ),
        ]

        # Save segment detections
        self.segment_detection_db_orm_manager.batch_save_segment_detections(segment_detections)

        # Verify they exist
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_video_id(self.video.id)
        assert len(segment_detections_db) == 2

        # Batch delete segment detections by video ID
        self.segment_detection_db_orm_manager.batch_delete_segment_detections_by_video_id(self.video.id)

        # Verify they're deleted
        segment_detections_db = self.segment_detection_db_orm_manager.get_segment_detections_by_video_id(self.video.id)
        assert len(segment_detections_db) == 0
