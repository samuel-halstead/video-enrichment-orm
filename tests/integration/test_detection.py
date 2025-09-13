import pytest

from video_enrichment_orm.managers.db_detection import db_detection_manager
from video_enrichment_orm.managers.db_entity import db_entity_manager
from video_enrichment_orm.managers.db_segment_detection import (
    db_segment_detection_manager,
)
from video_enrichment_orm.managers.db_taxonomy import db_taxonomy_manager
from video_enrichment_orm.managers.db_video import db_video_manager
from video_enrichment_orm.schemas.detection import DetectionCreate, DetectionUpdate
from video_enrichment_orm.schemas.entity import EntityCreate
from video_enrichment_orm.schemas.segment_detection import SegmentDetectionCreate
from video_enrichment_orm.schemas.taxonomy import TaxonomyCreate
from video_enrichment_orm.schemas.video import VideoCreate


class TestDetection:
    @classmethod
    def setup_class(cls):
        # run once before any tests in this class
        cls.detection_db_orm_manager = db_detection_manager
        cls.video_db_orm_manager = db_video_manager
        cls.taxonomy_db_orm_manager = db_taxonomy_manager
        cls.entity_db_orm_manager = db_entity_manager
        cls.segment_detection_db_orm_manager = db_segment_detection_manager

        # create one video, taxonomy, entity, and segment_detection for *all* tests
        cls.video = cls.video_db_orm_manager.save_video(
            VideoCreate(
                code="test_video_for_detection",
                path="/test/path/to/video.mp4",
                extension="mp4",
            )
        )

        cls.taxonomy = cls.taxonomy_db_orm_manager.save_taxonomy(
            TaxonomyCreate(
                label="test_taxonomy_for_detection",
                taxonomy_id=None,
            )
        )

        cls.entity = cls.entity_db_orm_manager.save_entity(
            EntityCreate(
                alias=["test_entity_for_detection"],
                enabled=True,
                taxonomy_id=cls.taxonomy.id,
            )
        )

        cls.segment_detection = cls.segment_detection_db_orm_manager.save_segment_detection(
            SegmentDetectionCreate(
                video_id=cls.video.id,
                start_frame=100,
                end_frame=200,
                taxonomy_id=cls.taxonomy.id,
                entity_id=cls.entity.id,
            )
        )

    @classmethod
    def teardown_class(cls):
        # run once after all tests in this class
        cls.segment_detection_db_orm_manager.delete_segment_detection_by_id(cls.segment_detection.id)
        cls.entity_db_orm_manager.delete_entity_by_id(cls.entity.id)
        cls.taxonomy_db_orm_manager.delete_taxonomy_by_id(cls.taxonomy.id)
        cls.video_db_orm_manager.delete_video_by_id(cls.video.id)

    @pytest.fixture(autouse=True)
    def cleanup_detections(self):
        # this runs after each test: tear down *any* detections that the test created
        yield
        for d in self.detection_db_orm_manager.get_detections_by_video_id(self.video.id):
            self.detection_db_orm_manager.delete_detection_by_id(d.id)

    def test_insert_and_delete_detection(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        assert detection.id is not None
        assert detection.uuid is not None
        assert detection.video_id == self.video.id
        assert detection.frame == 150
        assert detection.segment_detection_id == self.segment_detection.id
        assert detection.detection_score == 0.95
        assert detection.entity_score == 0.87
        assert detection.bbox_x_min == 0.1
        assert detection.bbox_y_min == 0.2
        assert detection.bbox_x_max == 0.8
        assert detection.bbox_y_max == 0.9

        # Delete detection
        self.detection_db_orm_manager.delete_detection_by_id(detection.id)

        with pytest.raises(ValueError):
            self.detection_db_orm_manager.get_detection_by_id(detection.id)

    def test_update_detection_by_id(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Update detection
        detection_update = DetectionUpdate(
            frame=160,
            detection_score=0.98,
            entity_score=0.92,
            bbox_x_min=0.15,
            bbox_y_min=0.25,
            bbox_x_max=0.85,
            bbox_y_max=0.95,
        )
        detection = self.detection_db_orm_manager.update_detection(detection_update, id=detection.id)

        assert detection.frame == 160
        assert detection.detection_score == 0.98
        assert detection.entity_score == 0.92
        assert detection.bbox_x_min == 0.15
        assert detection.bbox_y_min == 0.25
        assert detection.bbox_x_max == 0.85
        assert detection.bbox_y_max == 0.95
        assert detection.video_id == self.video.id
        assert detection.segment_detection_id == self.segment_detection.id

    def test_update_detection_by_uuid(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Update detection
        detection_update = DetectionUpdate(
            frame=170,
            detection_score=0.99,
            entity_score=0.94,
            bbox_x_min=0.2,
            bbox_y_min=0.3,
            bbox_x_max=0.9,
            bbox_y_max=1.0,
        )
        detection = self.detection_db_orm_manager.update_detection(detection_update, uuid=detection.uuid)

        assert detection.frame == 170
        assert detection.detection_score == 0.99
        assert detection.entity_score == 0.94
        assert detection.bbox_x_min == 0.2
        assert detection.bbox_y_min == 0.3
        assert detection.bbox_x_max == 0.9
        assert detection.bbox_y_max == 1.0
        assert detection.video_id == self.video.id
        assert detection.segment_detection_id == self.segment_detection.id

    def test_get_detection_by_id(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detection by ID
        detection_db = self.detection_db_orm_manager.get_detection_by_id(detection.id)
        assert detection_db.video_id == self.video.id
        assert detection_db.frame == 150
        assert detection_db.segment_detection_id == self.segment_detection.id
        assert detection_db.detection_score == 0.95
        assert detection_db.entity_score == 0.87
        assert detection_db.bbox_x_min == 0.1
        assert detection_db.bbox_y_min == 0.2
        assert detection_db.bbox_x_max == 0.8
        assert detection_db.bbox_y_max == 0.9

    def test_get_detection_by_uuid(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detection by UUID
        detection_db = self.detection_db_orm_manager.get_detection_by_uuid(detection.uuid)
        assert detection_db.video_id == self.video.id
        assert detection_db.frame == 150
        assert detection_db.segment_detection_id == self.segment_detection.id
        assert detection_db.detection_score == 0.95
        assert detection_db.entity_score == 0.87
        assert detection_db.bbox_x_min == 0.1
        assert detection_db.bbox_y_min == 0.2
        assert detection_db.bbox_x_max == 0.8
        assert detection_db.bbox_y_max == 0.9

    def test_get_detections_by_ids(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detections by IDs
        detections_db = self.detection_db_orm_manager.get_detections_by_ids([detection.id])
        assert len(detections_db) == 1
        assert detections_db[0].video_id == self.video.id
        assert detections_db[0].frame == 150
        assert detections_db[0].segment_detection_id == self.segment_detection.id
        assert detections_db[0].detection_score == 0.95
        assert detections_db[0].entity_score == 0.87

    def test_get_detections_by_uuids(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detections by UUIDs
        detections_db = self.detection_db_orm_manager.get_detections_by_uuids([detection.uuid])
        assert len(detections_db) == 1
        assert detections_db[0].video_id == self.video.id
        assert detections_db[0].frame == 150
        assert detections_db[0].segment_detection_id == self.segment_detection.id
        assert detections_db[0].detection_score == 0.95
        assert detections_db[0].entity_score == 0.87

    def test_get_detections_by_video_id(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detections by video ID
        detections_db = self.detection_db_orm_manager.get_detections_by_video_id(self.video.id)
        assert len(detections_db) == 1
        assert detections_db[0].id == detection.id
        assert detections_db[0].video_id == self.video.id

    def test_get_detections_by_segment_detection_id(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detections by segment detection ID
        detections_db = self.detection_db_orm_manager.get_detections_by_segment_detection_id(self.segment_detection.id)
        assert len(detections_db) == 1
        assert detections_db[0].id == detection.id
        assert detections_db[0].segment_detection_id == self.segment_detection.id

    def test_get_detections_by_frame(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detections by frame
        detections_db = self.detection_db_orm_manager.get_detections_by_frame(self.video.id, 150)
        assert len(detections_db) == 1
        assert detections_db[0].id == detection.id
        assert detections_db[0].frame == 150

    def test_get_detections_by_frame_range(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detections by frame range
        detections_db = self.detection_db_orm_manager.get_detections_by_frame_range(self.video.id, 100, 200)
        assert len(detections_db) == 1
        assert detections_db[0].id == detection.id
        assert detections_db[0].frame == 150

    def test_get_detections_by_score_threshold(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detections by score threshold
        detections_db = self.detection_db_orm_manager.get_detections_by_score_threshold(self.video.id, 0.9)
        assert len(detections_db) == 1
        assert detections_db[0].id == detection.id
        assert detections_db[0].detection_score == 0.95

    def test_get_detections_by_entity_score_threshold(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Get detections by entity score threshold
        detections_db = self.detection_db_orm_manager.get_detections_by_entity_score_threshold(self.video.id, 0.8)
        assert len(detections_db) == 1
        assert detections_db[0].id == detection.id
        assert detections_db[0].entity_score == 0.87

    def test_delete_detection_by_uuid(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Delete detection by UUID
        self.detection_db_orm_manager.delete_detection_by_uuid(detection.uuid)

        with pytest.raises(ValueError):
            self.detection_db_orm_manager.get_detection_by_uuid(detection.uuid)

    def test_delete_detections_by_video_id(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Delete detections by video ID
        self.detection_db_orm_manager.delete_detections_by_video_id(self.video.id)

        # Verify it's deleted
        detections_db = self.detection_db_orm_manager.get_detections_by_video_id(self.video.id)
        assert len(detections_db) == 0

    def test_delete_detections_by_segment_detection_id(self) -> None:
        # Create detection
        detection = DetectionCreate(
            video_id=self.video.id,
            frame=150,
            segment_detection_id=self.segment_detection.id,
            detection_score=0.95,
            entity_score=0.87,
            bbox_x_min=0.1,
            bbox_y_min=0.2,
            bbox_x_max=0.8,
            bbox_y_max=0.9,
        )
        detection = self.detection_db_orm_manager.save_detection(detection)

        # Delete detections by segment detection ID
        self.detection_db_orm_manager.delete_detections_by_segment_detection_id(self.segment_detection.id)

        # Verify it's deleted
        detections_db = self.detection_db_orm_manager.get_detections_by_segment_detection_id(self.segment_detection.id)
        assert len(detections_db) == 0

    def test_batch_save_detections(self) -> None:
        # Create multiple detections
        detections = [
            DetectionCreate(
                video_id=self.video.id,
                frame=150,
                segment_detection_id=self.segment_detection.id,
                detection_score=0.95,
                entity_score=0.87,
                bbox_x_min=0.1,
                bbox_y_min=0.2,
                bbox_x_max=0.8,
                bbox_y_max=0.9,
            ),
            DetectionCreate(
                video_id=self.video.id,
                frame=160,
                segment_detection_id=self.segment_detection.id,
                detection_score=0.92,
                entity_score=0.85,
                bbox_x_min=0.2,
                bbox_y_min=0.3,
                bbox_x_max=0.9,
                bbox_y_max=1.0,
            ),
        ]

        # Batch save detections
        saved_detections = self.detection_db_orm_manager.batch_save_detections(detections)

        assert len(saved_detections) == 2
        assert saved_detections[0].video_id == self.video.id
        assert saved_detections[0].frame == 150
        assert saved_detections[0].detection_score == 0.95
        assert saved_detections[1].video_id == self.video.id
        assert saved_detections[1].frame == 160
        assert saved_detections[1].detection_score == 0.92

    def test_batch_delete_detections_by_video_id(self) -> None:
        # Create multiple detections
        detections = [
            DetectionCreate(
                video_id=self.video.id,
                frame=150,
                segment_detection_id=self.segment_detection.id,
                detection_score=0.95,
                entity_score=0.87,
                bbox_x_min=0.1,
                bbox_y_min=0.2,
                bbox_x_max=0.8,
                bbox_y_max=0.9,
            ),
            DetectionCreate(
                video_id=self.video.id,
                frame=160,
                segment_detection_id=self.segment_detection.id,
                detection_score=0.92,
                entity_score=0.85,
                bbox_x_min=0.2,
                bbox_y_min=0.3,
                bbox_x_max=0.9,
                bbox_y_max=1.0,
            ),
        ]

        # Save detections
        self.detection_db_orm_manager.batch_save_detections(detections)

        # Verify they exist
        detections_db = self.detection_db_orm_manager.get_detections_by_video_id(self.video.id)
        assert len(detections_db) == 2

        # Batch delete detections by video ID
        self.detection_db_orm_manager.batch_delete_detections_by_video_id(self.video.id)

        # Verify they're deleted
        detections_db = self.detection_db_orm_manager.get_detections_by_video_id(self.video.id)
        assert len(detections_db) == 0

    def test_batch_delete_detections_by_segment_detection_id(self) -> None:
        # Create multiple detections
        detections = [
            DetectionCreate(
                video_id=self.video.id,
                frame=150,
                segment_detection_id=self.segment_detection.id,
                detection_score=0.95,
                entity_score=0.87,
                bbox_x_min=0.1,
                bbox_y_min=0.2,
                bbox_x_max=0.8,
                bbox_y_max=0.9,
            ),
            DetectionCreate(
                video_id=self.video.id,
                frame=160,
                segment_detection_id=self.segment_detection.id,
                detection_score=0.92,
                entity_score=0.85,
                bbox_x_min=0.2,
                bbox_y_min=0.3,
                bbox_x_max=0.9,
                bbox_y_max=1.0,
            ),
        ]

        # Save detections
        self.detection_db_orm_manager.batch_save_detections(detections)

        # Verify they exist
        detections_db = self.detection_db_orm_manager.get_detections_by_segment_detection_id(self.segment_detection.id)
        assert len(detections_db) == 2

        # Batch delete detections by segment detection ID
        self.detection_db_orm_manager.batch_delete_detections_by_segment_detection_id(self.segment_detection.id)

        # Verify they're deleted
        detections_db = self.detection_db_orm_manager.get_detections_by_segment_detection_id(self.segment_detection.id)
        assert len(detections_db) == 0
