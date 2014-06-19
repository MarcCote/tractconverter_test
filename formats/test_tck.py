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
from tractconverter.formats.header import Header as H

DATA_DIR = os.path.join(os.path.realpath(tractconverter.__path__[0]), "..", "tests", "data")


def test_write_file():
    f, filename = tempfile.mkstemp('_empty.tck')
    os.remove(filename)

    tck = FORMATS['tck']
    tck_file = tck.create(filename)

    assert_equal(len(tck(filename).load_all()), 0)
    assert_equal(tck_file.hdr[H.NB_FIBERS], 0)

    # Add one streamline to the file.
    tck_file += [np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype='<f4')]
    assert_equal(len(tck(filename).load_all()), 1)
    assert_equal(tck_file.hdr[H.NB_FIBERS], 1)

    # Add two more streamlines to the file.
    tck_file += [np.array([[1, 2, 3], [4, 5, 6]], dtype='<f4'),
                 np.array([[7, 8, 9], [0, 0, 0], [1, 1, 1]], dtype='<f4')]

    assert_equal(len(tck(filename).load_all()), 3)
    assert_equal(tck_file.hdr[H.NB_FIBERS], 3)


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
