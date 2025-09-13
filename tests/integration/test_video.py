import pytest

from video_enrichment_orm.dao.video import VideoStatus
from video_enrichment_orm.managers.db_video import db_video_manager
from video_enrichment_orm.schemas.video import VideoCreate, VideoUpdate


class TestVideo:
    @classmethod
    def setup_class(cls):
        # run once before any tests in this class
        cls.video_db_orm_manager = db_video_manager

    @classmethod
    def teardown_class(cls):
        # run once after all tests in this class
        pass

    @pytest.fixture(autouse=True)
    def cleanup_videos(self):
        # this runs after each test: tear down *any* videos that the test created
        yield
        for v in self.video_db_orm_manager.get_videos():
            self.video_db_orm_manager.delete_video_by_id(v.id)

    def test_insert_and_delete_video(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        assert video.id is not None
        assert video.uuid is not None
        assert video.code == "test_video"
        assert video.path == "test_path"
        assert video.extension == "mp4"
        assert video.status == VideoStatus.PENDING

        # Delete video
        self.video_db_orm_manager.delete_video_by_id(video.id)

        with pytest.raises(ValueError):
            self.video_db_orm_manager.get_video_by_id(video.id)

    def test_update_video_by_id(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        video_update = VideoUpdate(
            code="test_video_updated",
            path="test_path_updated",
            extension="mp5",
        )
        video = self.video_db_orm_manager.update_video(video_update, id=video.id)

        assert video.code == "test_video_updated"
        assert video.path == "test_path_updated"
        assert video.extension == "mp5"

    def test_update_video_by_uuid(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        video_update = VideoUpdate(
            code="test_video_updated",
            path="test_path_updated",
            extension="mp5",
        )
        video = self.video_db_orm_manager.update_video(video_update, uuid=video.uuid)

        assert video.code == "test_video_updated"
        assert video.path == "test_path_updated"
        assert video.extension == "mp5"

    def test_get_video_by_id(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        video_db = self.video_db_orm_manager.get_video_by_id(video.id)
        assert video_db.code == "test_video"
        assert video_db.path == "test_path"
        assert video_db.extension == "mp4"

    def test_get_video_by_uuid(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        video_db = self.video_db_orm_manager.get_video_by_uuid(video.uuid)
        assert video_db.code == "test_video"
        assert video_db.path == "test_path"
        assert video_db.extension == "mp4"

    def test_get_videos(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        videos_db = self.video_db_orm_manager.get_videos()
        assert len(videos_db) == 1
        assert videos_db[0].code == "test_video"
        assert videos_db[0].path == "test_path"
        assert videos_db[0].extension == "mp4"

    def test_get_videos_by_ids(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        videos_db = self.video_db_orm_manager.get_videos_by_ids([video.id])
        assert len(videos_db) == 1
        assert videos_db[0].code == "test_video"
        assert videos_db[0].path == "test_path"
        assert videos_db[0].extension == "mp4"

    def test_get_videos_by_uuids(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        videos_db = self.video_db_orm_manager.get_videos_by_uuids([video.uuid])
        assert len(videos_db) == 1
        assert videos_db[0].code == "test_video"
        assert videos_db[0].path == "test_path"
        assert videos_db[0].extension == "mp4"

    def test_delete_video_by_uuid(self) -> None:
        video = VideoCreate(
            code="test_video",
            path="test_path",
            extension="mp4",
        )
        video = self.video_db_orm_manager.save_video(video)

        self.video_db_orm_manager.delete_video_by_uuid(video.uuid)

        with pytest.raises(ValueError):
            self.video_db_orm_manager.get_video_by_uuid(video.uuid)
