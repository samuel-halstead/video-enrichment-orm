"""Global pytest config."""

import secrets

seed = secrets.randbelow(1_000_000)


def pytest_report_header() -> str:
    """Adding info in report header."""
    return f"Test seed: {seed}"
