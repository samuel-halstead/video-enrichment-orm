"""Package related tests."""


def test_import() -> None:
    """Test basic import."""
    import importlib

    try:
        importlib.import_module("video_enrichment_orm")
    except ImportError:
        raise AssertionError() from None
