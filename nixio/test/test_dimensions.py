# -*- coding: utf-8 -*-
# Copyright © 2014, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
import os
import unittest
import numpy as np

import nixio as nix
from .tmp import TempDir


test_range = tuple([float(i) for i in range(10)])
test_sampl = 0.1
test_label = "test label"
test_labels = tuple([str(i) + "_label" for i in range(10)])


class TestDimension(unittest.TestCase):

    def setUp(self):
        self.tmpdir = TempDir("dimtest")
        self.testfilename = os.path.join(self.tmpdir.path, "dimtest.nix")
        self.file = nix.File.open(self.testfilename, nix.FileMode.Overwrite)
        self.block = self.file.create_block("test block", "recordingsession")
        self.array = self.block.create_data_array("test array", "signal",
                                                  nix.DataType.Float, (0, ))

        self.set_dim = self.array.append_set_dimension()
        self.sample_dim = self.array.append_sampled_dimension(test_sampl)
        self.range_dim = self.array.append_range_dimension(test_range)

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()
        self.tmpdir.cleanup()

    def test_set_dimension(self):
        assert(self.set_dim.index == 1)
        assert(self.set_dim.dimension_type == nix.DimensionType.Set)
        assert(self.array.dimensions[0].index == 1)

        assert(self.set_dim.labels == ())
        self.set_dim.labels = test_labels
        assert(self.set_dim.labels == test_labels)

    def test_sample_dimension(self):
        assert(self.sample_dim.index == 2)
        assert(self.sample_dim.dimension_type == nix.DimensionType.Sample)
        assert(self.array.dimensions[1].index == 2)

        assert(self.sample_dim.label is None)
        self.sample_dim.label = test_label
        assert(self.sample_dim.label == test_label)
        self.sample_dim.label = None
        assert(self.sample_dim.label is None)

        assert(self.sample_dim.unit is None)
        self.sample_dim.unit = "mV"
        assert(self.sample_dim.unit == "mV")
        self.sample_dim.unit = None
        assert(self.sample_dim.unit is None)

        assert(self.sample_dim.sampling_interval == test_sampl)
        self.sample_dim.sampling_interval = 1.123
        assert(self.sample_dim.sampling_interval == 1.123)

        assert(self.sample_dim.offset is None)
        self.sample_dim.offset = 0.3
        assert(self.sample_dim.offset == 0.3)
        self.sample_dim.offset = None
        assert(self.sample_dim.offset is None)

        self.sample_dim.sampling_interval = 2.
        self.sample_dim.offset = 3.

        assert(self.sample_dim.index_of(3.14) == 0)
        assert(self.sample_dim.index_of(23.) == 10)
        assert(type(self.sample_dim.index_of(23.) == int))

        assert(self.sample_dim.position_at(0) == 3.)
        assert(self.sample_dim.position_at(200) == 200*2.+3.)

        assert(len(self.sample_dim.axis(10)) == 10)
        assert(self.sample_dim.axis(10)[0] == 3.)
        assert(self.sample_dim.axis(10)[-1] == 9*2.+3.)

        assert(len(self.sample_dim.axis(10, 2)) == 10)
        assert(self.sample_dim.axis(10, 2)[0] == 2 * 2. + 3.)
        assert(self.sample_dim.axis(10, 2)[-1] == (9 + 2) * 2. + 3.)

    def test_range_dimension(self):
        assert(self.range_dim.index == 3)
        assert(self.range_dim.dimension_type == nix.DimensionType.Range)
        assert(self.array.dimensions[2].index == 3)

        assert(self.range_dim.label is None)
        self.range_dim.label = test_label
        assert(self.range_dim.label == test_label)
        self.range_dim.label = None
        assert(self.range_dim.label is None)

        assert(self.range_dim.unit is None)
        self.range_dim.unit = "mV"
        assert(self.range_dim.unit == "mV")
        self.range_dim.unit = None
        assert(self.range_dim.unit is None)

        assert(self.range_dim.ticks == test_range)
        other = tuple([i*3.14 for i in range(10)])
        self.range_dim.ticks = other
        assert(self.range_dim.ticks == other)

        assert(self.range_dim.index_of(0.) == 0)
        assert(self.range_dim.index_of(10.) == (np.floor(10./3.14)))
        assert(self.range_dim.index_of(100.) == 9)
        assert(self.range_dim.index_of(-100.) == 0)

        assert(self.range_dim.tick_at(0) == 0)
        assert(self.range_dim.tick_at(9) == other[-1])
        with self.assertRaises(IndexError):
            self.range_dim.tick_at(100)

        assert(self.range_dim.axis(10) == other)
        assert(self.range_dim.axis(2) == other[:2])
        assert(self.range_dim.axis(2, 2) == other[2:4])
        with self.assertRaises(IndexError):
            self.range_dim.axis(10, 2)
            self.range_dim.axis(100)

    def test_alias_dimension(self):
        da = self.block.create_data_array("alias da", "dimticks",
                                          data=np.random.random(10))
        da.label = "alias dimension label"
        da.unit = "F"
        da.append_alias_range_dimension()
        assert(len(da.dimensions) == 1)
        assert(da.dimensions[0].label == da.label)
        assert(da.dimensions[0].unit == da.unit)
        assert(np.all(da.dimensions[0].ticks == da[:]))

    def test_set_dim_label_resize(self):
        setdim = self.array.append_set_dimension()
        labels = ["A", "B"]
        setdim.labels = labels
        assert tuple(labels) == setdim.labels

        newlabels = ["C", "B", "A"]
        setdim.labels = newlabels
        assert tuple(newlabels) == setdim.labels

    def test_range_dim_ticks_resize(self):
        rangedim = self.array.append_range_dimension([1, 2, 100])
        ticks = [1, 1, 30]
        rangedim.ticks = ticks
        assert tuple(ticks) == rangedim.ticks

        newticks = [2, 4, 300, 800]
        rangedim.ticks = newticks
        assert tuple(newticks) == rangedim.ticks

    def test_append_dim_init(self):
        slabels = ["label A", "label B"]
        setdim = self.array.append_set_dimension(slabels)
        assert tuple(slabels) == setdim.labels

        rticks = [1, 2, 10.3]
        rlabel = "range-label"
        runit = "ms"
        rdim = self.array.append_range_dimension(rticks, rlabel, runit)
        assert tuple(rticks) == rdim.ticks
        assert rlabel == rdim.label
        assert runit == rdim.unit

        sinterval = 0.25
        slabel = "sample label"
        sunit = "us"
        soffset = 10
        smpldim = self.array.append_sampled_dimension(sinterval,
                                                      slabel,
                                                      sunit,
                                                      soffset)
        assert sinterval == smpldim.sampling_interval
        assert slabel == smpldim.label
        assert sunit == smpldim.unit
        assert soffset == smpldim.offset
