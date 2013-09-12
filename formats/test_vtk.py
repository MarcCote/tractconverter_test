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

def compare_data(input_1, input_2):
    for i, (f1, f2) in enumerate(zip(input_1, input_2)):
        assert_array_almost_equal(f1, f2)


def test_load_file():
    #Load empty file
    filename = os.path.join(DATA_DIR, "empty.vtk")
    in_format = tractconverter.FORMATS['vtk']
    in_format(filename)

    #Load binary file
    filename = os.path.join(DATA_DIR, "uncinate.vtk")
    in_format = tractconverter.FORMATS['vtk']
    in_format(filename)

    #Load ascii file
    filename = os.path.join(DATA_DIR, "ascii.vtk")
    in_format = tractconverter.FORMATS['vtk']
    in_format(filename)
    

def test_convert_ascii_file():
    rng = np.random.RandomState(42)
    # Create 10 fake streamlines
    streamlines = []
    nb_points_per_streamline = rng.randint(5,20,(10))
    for nb_points in nb_points_per_streamline:
        streamlines.append(rng.rand(nb_points, 3) * 10)

    # Create VTK ascii file
    f, out = tempfile.mkstemp()
    os.remove(out)
    with open(out + '_ascii.vtk', 'wb') as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("Automatically generated ASCII vtk file\n")
        f.write("ASCII\n")
        f.write("DATASET POLYDATA\n")

        f.write("\n")
        total_nb_points = sum(map(len, streamlines))
        f.write("POINTS {0} {1}\n".format(total_nb_points, "float"))
        for s in streamlines:
            for p in s:
                f.write("{0} {1} {2}\n".format(*p))

        f.write("\n")
        nb_lines = len(streamlines)
        size = total_nb_points + nb_lines
        f.write("LINES {0} {1}\n".format(nb_lines, size))
        cpt_points = 0
        for s in streamlines:
            nb_points = len(s)
            line_points = " ".join(map(str, range(cpt_points, cpt_points + nb_points)))
            f.write("{0} {1}\n".format(nb_points, line_points))
            cpt_points += nb_points

    # Test conversion ascii to binary
    format = tractconverter.FORMATS['vtk']
    ref_filename = out + '_ascii.vtk'
    out_filename = out + '_binary.vtk'

    input = format(ref_filename, None)
    output = format.create(out_filename, input.hdr, None)
    tractconverter.convert(input, output)

    input = format(ref_filename, None)
    output = format(out_filename, None)
    compare_data(input, output)

    input = format(ref_filename, None)
    compare_data(input, streamlines)
    output = format(out_filename, None)
    compare_data(output, streamlines)

    os.remove(ref_filename)
    os.remove(out_filename)


if __name__ == "__main__":
    test_load_file()
    test_convert_ascii_file()