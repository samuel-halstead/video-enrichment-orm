from typing import Any, Iterator


def batch_items(items: list[Any], batch_size: int) -> Iterator[list[Any]]:
    """Yield successive batches from a list of items."""
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]
