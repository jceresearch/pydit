""" Pytest configuration file , inspired in the one used by pyjanitor"""

import pytest

TEST_DATA_DIR = "tests/test_data"
EXAMPLES_DIR = "examples/"


def pytest_configure():
    """pytest configuration"""
    pytest.TEST_DATA_DIR = TEST_DATA_DIR
    pytest.EXAMPLES_DIR = EXAMPLES_DIR
