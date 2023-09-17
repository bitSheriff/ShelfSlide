# import the test framework
import pytest
from unittest.mock import MagicMock

# import the code to be tested
import sys
sys.path.append("..")
import shelfslide

def test_load_simple_bookLibrary():

    list = shelfslide.load_simple_bookLibrary(".")

    # list must be empty
    assert len(list) == 0

    pass