"""Test pymsx

Test package level functionality.
"""

from pymsx import __version__


def test_version() -> None:
    """Test package version number"""
    assert __version__ == "0.0.1"


if __name__ == "__main__":
    test_version()
