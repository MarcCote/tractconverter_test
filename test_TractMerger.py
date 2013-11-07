from pdb import set_trace as dbg

import os
import copy
import tempfile
import hashlib
from functools import partial

from numpy.testing import (assert_equal,
                           assert_almost_equal,
                           assert_array_equal,
                           assert_array_almost_equal,
                           assert_raises)

import tractconverter
from tractconverter import FORMATS
from tractconverter.formats.header import Header

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "data" + os.sep


def compare_data(input_1, input_2):
    for i, (f1, f2) in enumerate(zip(input_1, input_2)):
        assert_array_equal(f1, f2)


def test_merge_empty_file():
    #Load test data
    TRK = FORMATS['trk']
    test_file = TRK(DATA_DIR + "uncinate.trk")
    empty_file = TRK(DATA_DIR + "empty.trk")

    f, out = tempfile.mkstemp('_empty_merge')
    os.remove(out)
    out_filename = out + ".trk"
    print out_filename
    out_file = TRK.create(out_filename, copy.deepcopy(test_file.hdr))
    tractconverter.merge([empty_file, test_file], out_file)

    merged_file = TRK(out_filename)
    compare_data(merged_file, test_file)
    os.remove(out_filename)

def test_merge_file():
    #Load test data
    TRK = FORMATS['trk']
    test1_file = TRK(DATA_DIR + "uncinate.trk")
    test2_file = TRK(DATA_DIR + "uncinate.trk")

    f, out = tempfile.mkstemp('_merge')
    os.remove(out)
    out_filename = out + ".trk"
    out_file = TRK.create(out_filename, copy.deepcopy(test1_file.hdr))
    tractconverter.merge([test1_file, test2_file], out_file)

    merged_file = TRK(out_filename)
    assert_equal(merged_file.hdr[Header.NB_FIBERS],
                 test1_file.hdr[Header.NB_FIBERS] + test2_file.hdr[Header.NB_FIBERS])

    streamlines = []
    streamlines += [s for s in test1_file]
    streamlines += [s for s in test2_file]
    compare_data(merged_file, streamlines)
    os.remove(out_filename)

if __name__ == "__main__":
    test_merge_empty_file()
    test_merge_file()
