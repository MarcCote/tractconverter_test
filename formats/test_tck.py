from pdb import set_trace as dbg

import os
import tempfile
import hashlib
import numpy as np
from functools import partial

from numpy.testing import (assert_equal,
                           assert_almost_equal,
                           assert_array_equal,
                           assert_array_almost_equal,
                           assert_raises)

import tractconverter
from tractconverter import FORMATS

DATA_DIR = os.path.join(os.path.realpath(tractconverter.__path__[0]), "..", "tests", "data")


def test_load_file():
    #Load empty file
    filename = os.path.join(DATA_DIR, "empty.tck")
    in_format = tractconverter.FORMATS['tck']
    for i in in_format(filename): pass  # Check if we can iterate throught the streamlines.

    #Load binary file
    filename = os.path.join(DATA_DIR, "uncinate.tck")
    in_format = tractconverter.FORMATS['tck']
    in_format(filename)
    for i in in_format(filename): pass  # Check if we can iterate throught the streamlines.
    

if __name__ == "__main__":
    test_load_file()