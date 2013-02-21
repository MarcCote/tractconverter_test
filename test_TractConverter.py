from pdb import set_trace as dbg

import os
import tempfile
import hashlib
from functools import partial

import numpy as np

from numpy.testing import (assert_equal,
                           assert_almost_equal,
                           assert_array_equal,
                           assert_array_almost_equal,
                           assert_raises)


import tractconverter.TractConverter as TractConverter
from tractconverter.TractConverter import FORMATS

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "data" + os.sep


def compare_data(input_1, input_2):

    for i, (f1, f2) in enumerate(zip(input_1, input_2)):
        assert_array_equal(f1, f2)


def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)

    return d.hexdigest()


def test_conversion():
    #Load test data
    ref = DATA_DIR + "uncinate"
    ref_anat = DATA_DIR + "anat.nii.gz"

    #Test every possible conversions
    for k1 in FORMATS.keys():
        for k2 in FORMATS.keys():
            print "Testing {0}2{1}".format(k1, k2)
            f, out = tempfile.mkstemp('_{0}2{1}'.format(k1, k2))

            input = ref + "." + k1
            output = out + "." + k2
            TractConverter.convert(input, output, ref_anat)

            f2, out2 = tempfile.mkstemp('_{0}2{1}'.format(k2, k1))
            output2 = out2 + "." + k1
            TractConverter.convert(output, output2, ref_anat)

            #assert_equal(md5sum(input), md5sum(output2))
            compare_data(FORMATS[k1](input, ref_anat), FORMATS[k2](output, ref_anat))
            os.remove(output)

            compare_data(FORMATS[k1](input, ref_anat), FORMATS[k1](output2, ref_anat))
            os.remove(output2)


if __name__ == "__main__":
    test_conversion()
