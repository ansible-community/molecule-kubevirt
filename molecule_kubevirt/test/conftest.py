"""Pytest Fixtures."""
import pytest


@pytest.fixture
def DRIVER():
    """Return name of the driver to be tested."""
    return "kubevirt"


import os
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def change_dir(path: Path):
    previous_path = Path.cwd()

    os.chdir(path)
    yield
    os.chdir(previous_path)