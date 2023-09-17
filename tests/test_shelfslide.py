
import sys
sys.path.append("..")
#from shelfslide import *
import shelfslide

def test_load_simple_bookLibrary():

    list = shelfslide.load_simple_bookLibrary(".")

    # list must be empty
    assert len(list) == 0

    pass