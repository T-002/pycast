#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Copyright (c) 2012 Christian Schwarz
#
#Permission is hereby granted, free of charge, to any person obtaining
#a copy of this software and associated documentation files (the
#"Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish,
#distribute, sublicense, and/or sell copies of the Software, and to
#permit persons to whom the Software is furnished to do so, subject to
#the following conditions:
#
#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## required external modules
from nose import with_setup
import unittest, re, os
from copy import copy

## required modules from pycast
from pycast.common.timeseries import TimeSeries, FusionMethods
from pycast.methods.basemethod import BaseMethod

class TimeSeriesMiscellaneousTest(unittest.TestCase):
    """Test class containing tests for miscallaneous TimeSeries functions."""

    def setUp(self):
        """Initializes the environment for each test."""

    def tearDown(self):
        """This function gets called after each test function."""
        if os.path.isfile("temp_plot.dat"):
            os.remove("temp_plot.dat")

    def method_test(self):
        """Test if TimeSeries apply branches work correctly.

        This is mainly to increase code coverage."""
        mOne   = BaseMethod([], hasToBeSorted=True, hasToBeNormalized=True)
        mTwo   = BaseMethod([], hasToBeSorted=False, hasToBeNormalized=True)
        mThree = BaseMethod([], hasToBeSorted=True, hasToBeNormalized=False)
        mFour  = BaseMethod([], hasToBeSorted=False, hasToBeNormalized=False)

        ts = TimeSeries(isNormalized=True)
        ts.add_entry(0.0, 0.0)
        ts.add_entry(0.1, 0.1)
        ts.add_entry(0.2, 0.2)
        ts.add_entry(0.3, 0.3)
        ts.add_entry(0.4, 0.4)

        try:
            ts.apply(mOne)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            ts.apply(mTwo)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            ts.apply(mThree)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            ts.apply(mFour)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

    def validity_of___str___test(self):
        """Test the validity of __str__ for a given TimeSeries."""
        ts = TimeSeries()
        ts.add_entry(0.0, 0.0)
        ts.add_entry(0.1, 0.1)
        ts.add_entry(0.2, 0.2)
        ts.add_entry(0.3, 0.3)
        ts.add_entry(0.4, 0.4)

        matchres = re.match("TimeSeries\(\[(.*)\]\)", ts.__str__())
        
        assert (None != matchres)

    def json_serialization_formatfree_test(self):
        """Test the json serialialization without predefined format."""
        tsOrg = TimeSeries()
        tsOrg.add_entry(0.0, 0.0)
        tsOrg.add_entry(0.1, 0.1)
        tsOrg.add_entry(0.2, 0.2)
        tsOrg.add_entry(0.3, 0.3)
        tsOrg.add_entry(0.4, 0.4)
        json = tsOrg.to_json()

        tsNew = TimeSeries.from_json(json)

        if not (len(tsOrg) == len(tsNew)): raise AssertionError
        if not (tsOrg == tsNew):           raise AssertionError

    def json_serialization_format_test(self):
        """Test the json serialialization with predefined format."""
        tsOrg = TimeSeries()
        tsOrg.add_entry(0.0, 0.0)
        tsOrg.add_entry(1.0, 0.1)
        tsOrg.add_entry(2.0, 0.2)
        tsOrg.add_entry(3.0, 0.3)
        tsOrg.add_entry(4.0, 0.4)
        tsOrg.set_timeformat("%Y-%m-%d_%H:%M:%S")
        json = tsOrg.to_json()

        tsNew = TimeSeries.from_json(json, format="%Y-%m-%d_%H:%M:%S")

        if not (len(tsOrg) == len(tsNew)): raise AssertionError
        if not (tsOrg == tsNew):          raise AssertionError

    def list_initialization_test(self):
        """Test TimeSeries initialization from a given list."""
        data = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]

        tsOne = TimeSeries()
        for entry in data:
            tsOne.add_entry(*entry)

        tsTwo = TimeSeries.from_twodim_list(data)

        if not (len(tsOne) == len(tsTwo)): raise AssertionError
        if not (tsOne == tsTwo):          raise AssertionError

    def list_serialization_formatfree_test(self):
        """Test the format free list serialization."""
        data = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = TimeSeries.from_twodim_list(data)

        data = tsOne.to_twodim_list()
        tsTwo = TimeSeries.from_twodim_list(data)

        assert tsOne == tsTwo

    def list_serialization_format_test(self):
        """Test the list serialization including time foramtting instructions."""
        data = [[0.0, 0.0], [1.0, 0.1], [2.0, 0.2], [3.0, 0.3], [4.0, 0.4], [5.0, 0.5]]
        tsOne = TimeSeries.from_twodim_list(data)

        tsOne.set_timeformat("%Y-%m-%d_%H:%M:%S")
        data = tsOne.to_twodim_list()
        tsTwo = TimeSeries.from_twodim_list(data, format="%Y-%m-%d_%H:%M:%S")

        assert tsOne == tsTwo

    def equal_test(self):
        """Test the == operator for TimeSeries instances."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        
        tsOne   = TimeSeries.from_twodim_list(data)
        tsTwo   = TimeSeries.from_twodim_list(data)
        tsThree = TimeSeries.from_twodim_list(data[:-2])
        tsFour  = TimeSeries.from_twodim_list(data)
        tsFive  = TimeSeries.from_twodim_list(data)

        tsFour[1][0] = 1.3
        tsFive[1][1] = 1.3

        if not (tsOne == tsTwo): raise AssertionError
        if (tsOne == tsThree):   raise AssertionError
        if (tsTwo == tsThree):   raise AssertionError
        if (tsOne == tsFour):    raise AssertionError
        if (tsOne == tsFive):    raise AssertionError
        if (tsThree == tsFour):  raise AssertionError
        if (tsThree == tsFive):  raise AssertionError
        if (tsFour == tsFive):   raise AssertionError

    def gnuplot_serialization_without_format_test(self):
        """Test serialization of timeSeries into gnuplot file."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = TimeSeries.from_twodim_list(data)
        tsOne.to_gnuplot_datafile("temp_plot.dat")
        
        assert os.path.isfile("temp_plot.dat")

    def gnuplot_serialization_with_format_test(self):
        """Test serialization of timeSeries into gnuplot file."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = TimeSeries.from_twodim_list(data)
        tsOne.set_timeformat("%Y-%m-%d_%H:%M:%S")
        tsOne.to_gnuplot_datafile("temp_plot.dat")
        
        assert os.path.isfile("temp_plot.dat")

    def gnuplot_serialization_exception_handling_test(self):
        """Test serialization of timeSeries into gnuplot file."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = TimeSeries.from_twodim_list(data)
        tsOne.to_gnuplot_datafile(None)

    def timeseries_sort_test(self):
        """Tests the sort_timeseries function."""
        data = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        ts   = TimeSeries.from_twodim_list(data)
        
        ts.sort_timeseries()
        ts.sort_timeseries(False)

        ts = TimeSeries(isSorted=True)
        ts.sort_timeseries()

    def timeseries_sorted_test(self):
        """Test the sorted_timeseries function."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = TimeSeries.from_twodim_list(data)
        
        tsTwo = tsOne.sorted_timeseries()

        if not (tsOne == tsTwo): raise AssertionError

        tsThree = tsOne.sorted_timeseries(False)

        if not tsOne == tsThree: raise AssertionError
        if not tsTwo == tsThree: raise AssertionError

    def timeseries___setitem___test(self):
        """Test TimeSeries.__setitem__"""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = TimeSeries.from_twodim_list(data)
        tsTwo = TimeSeries.from_twodim_list(data)

        tsTwo[1] = [0.2, 0.4]
        if tsOne == tsTwo: raise AssertionError

    def timeseries_iterator_test(self):
        """Test iteration over TimeSeries."""
        data = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        ts   = TimeSeries.from_twodim_list(data)

        idx = 0
        for entry in ts:
            if not entry[0] == data[idx][0]: raise AssertionError
            if not entry[1] == data[idx][1]: raise AssertionError
            idx += 1

    def addition_test(self):
        """Test the addition operator for TimeSeries instances."""
        dataOne = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        dataTwo = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        dataThree = dataOne + dataTwo
        dataThree.sort(key=lambda item:item[0])

        tsOne = TimeSeries.from_twodim_list(dataOne)
        tsTwo = TimeSeries.from_twodim_list(dataTwo)
        tsThree = TimeSeries.from_twodim_list(dataThree)

        if not tsThree == tsOne + tsTwo: raise AssertionError

    def is_normalized_test(self):
        """Test TimeSeries.is_normalized()."""
        ts = TimeSeries(isNormalized=True)
        assert ts.is_normalized()
        ts = TimeSeries(isNormalized=False)
        assert ts.is_normalized()
        ts.add_entry(0.1, 3.2)
        ts.add_entry(0.4, 3.2)
        ts.add_entry(0.3, 3.2)
        assert False == ts.is_normalized()


    def normalize_test(self):
        """Test timeseries normalization."""
        dataOne = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [5.1, 5.0]]
        dataTwo = [[0.5, 0.0], [1.5, 1.0], [2.5, 2.0], [3.5, 3.0], [4.5, 4.0], [5.5, 5.0]]

        tsOne   = TimeSeries.from_twodim_list(dataOne)
        tsTwo   = TimeSeries.from_twodim_list(dataTwo)
        
        tsOne.normalize("second")

        if not len(tsOne) == len(tsTwo): raise AssertionError
        if not tsOne == tsTwo:           raise AssertionError

    def normalize_complicated_test(self):
        """Test timeseries normalization."""
        dataOne = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [5.0, 5.0]]
        dataTwo = [[0.5, 0.0], [1.5, 1.0], [2.5, 2.0], [3.5, 3.0], [4.5, 4.0], [5.5, 5.0]]

        tsOne   = TimeSeries.from_twodim_list(dataOne)
        tsTwo   = TimeSeries.from_twodim_list(dataTwo)
        
        tsOne.normalize("second")
        tsOne.normalize("second")
        
        if not len(tsOne) == len(tsTwo):  raise AssertionError
        if not tsOne == tsTwo:            raise AssertionError

    def normalization_illegal_parameter_test(self):
        """Test illegal parameter of TimeSeries.normalize()."""
        data = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [5.0, 5.0]]
        ts   = TimeSeries.from_twodim_list(data)

        try:
            ts.normalize(normalizationLevel="ILLEGAL_PARAMETER")
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            ts.normalize(fusionMethod="ILLEGAL_PARAMETER")
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            ts.normalize(interpolationMethod="ILLEGAL_PARAMETER")
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

    def sum_fusion_method_test(self):
        """Testing the sum fusion method."""
        data  = [1,2,3,4,5,6,0,7]
        data2 = [1,3,5,65,3,2,1,34,0.5]
        
        assert FusionMethods["sum"](data)  == 28
        assert FusionMethods["sum"](data2) == 114.5
    
    def median_fusion_method_test(self):
        """Testing the median fusion method."""
        data0 = [3]
        data1 = [0,1,2,3,4,5,6,7]
        data2 = [0,1,8,7,3,4,5,2,6]
        data3 = [2,0.5,0.5,34,1,5,1,3,3,65]

        assert FusionMethods["median"](data0) == 3
        assert FusionMethods["median"](data1) == 4
        assert FusionMethods["median"](data2) == 4
        assert FusionMethods["median"](data3) == 3
    
    def mean_fusion_method_test(self):
        """Testing the average fusion method."""
        data0 = [3]
        data1 = [0,1,2,3,4,5,6,7]
        data2 = [0,1,8,7,3,4,5,2,6]
        data3 = [2,0.5,0.5,34,1,5,1,3,3,65]

        assert str(FusionMethods["mean"](data0))[:6] == "3.0"
        assert str(FusionMethods["mean"](data1))[:6] == "3.5"
        assert str(FusionMethods["mean"](data2))[:6] == "4.0"
        assert str(FusionMethods["mean"](data3))[:6] == "11.5"

    def copy_test(self):
        """Test TimeSeries cloning."""
        ts = TimeSeries.from_twodim_list([[0.5, 0.0], [1.5, 1.0], [2.5, 2.0], [3.5, 3.0], [4.5, 4.0], [5.5, 5.0]])
        tsClone = copy(ts)

        assert tsClone == ts
        
        ts[0][0] = 0.0
        assert ts != tsClone

        ts.add_entry(0.0, 1.1)
        assert len(ts) > len(tsClone)

    def normalized_method_requirement_test(self):
        """Test for StandardError."""
        def nothing(self):
            return

        data = [[0.0, 0.0], [1.1, 1.0], [2.0, 2.0], [5.0, 5.0]]
        ts   = TimeSeries.from_twodim_list(data)

        mOne   = BaseMethod([], hasToBeSorted=True, hasToBeNormalized=True)
        mOne.execute = nothing

        try:
            ts.apply(mOne)
        except StandardError:
            pass
        else:
            assert False    # pragma: no cover

        ts.normalize("second")
        ts.apply(mOne)







