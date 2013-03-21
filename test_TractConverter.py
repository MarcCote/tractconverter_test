from pdb import set_trace as dbg

import os
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
    anat_filename = DATA_DIR + "anat.nii.gz"

    #Test every possible conversions
    for k1, ref_format in FORMATS.items():
        for k2, out_format in FORMATS.items():
            print "Testing {0}2{1}".format(k1, k2)
            f, out = tempfile.mkstemp('_{0}2{1}'.format(k1, k2))

            ref_filename = ref + "." + k1
            out_filename = out + "." + k2

            input = ref_format(ref_filename, anat_filename)
            output = out_format.create(out_filename, input.hdr, anat_filename)
            tractconverter.convert(input, output)

            f, bak = tempfile.mkstemp('_{0}2{1}'.format(k2, k1))
            bak_filename = bak + "." + k1

            output = out_format(out_filename, anat_filename)
            backup = ref_format.create(bak_filename, input.hdr, anat_filename)
            tractconverter.convert(output, backup)

            input = ref_format(ref_filename, anat_filename)
            output = out_format(out_filename, anat_filename)
            compare_data(input, output)
            os.remove(out_filename)

            input = ref_format(ref_filename, anat_filename)
            backup = ref_format(bak_filename, anat_filename)
            compare_data(input, backup)
            os.remove(bak_filename)


if __name__ == "__main__":
    test_conversion()
