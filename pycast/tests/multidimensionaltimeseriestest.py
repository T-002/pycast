#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Copyright (c) 2012-2015 Christian Schwarz
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

## Tests concerning the database connection of pycast.common.TimeSeries
## SQLite is used for connector tests

## required external modules
import unittest, os
from copy import copy

from pycast.common.timeseries import MultiDimensionalTimeSeries

class MultiDimensionalTimeSeriesTest(unittest.TestCase):
    """"Tests the MultiDimensionalTimeSeries."""

    def initialization_error_test(self):
        """Test for the ValueError raised by the MultiDimensionalTimeSeries."""
        MultiDimensionalTimeSeries(1)
        MultiDimensionalTimeSeries(4)
        try:
            MultiDimensionalTimeSeries(0)
        except ValueError:
            pass    # pragma: no cover

        try:
            MultiDimensionalTimeSeries(-4)
        except ValueError:
            pass    # pragma: no cover

    def dimension_count_test(self):
        """Test the dimension count."""
        assert MultiDimensionalTimeSeries(3).dimension_count() == 3
        assert MultiDimensionalTimeSeries(3).dimension_count() < 4
        assert MultiDimensionalTimeSeries(40).dimension_count() > 2

    def add_entry_error_test(self):
        """Test ValueError of MultiDimensionalTimeSeries.add_entry(...)."""
        MultiDimensionalTimeSeries(3).add_entry(1, [1,2,3])
        MultiDimensionalTimeSeries(4).add_entry(1, [1,2,3,4])
        
        try:
            MultiDimensionalTimeSeries(3).add_entry(1, [1,2])
        except ValueError:
            pass    # pragma: no cover

        try:
            MultiDimensionalTimeSeries(3).add_entry(1, [1,2,3,4])
        except ValueError:
            pass    # pragma: no cover

        MultiDimensionalTimeSeries

    def add_entry_test(self):
        """Test MultiDimensionalTimeSeries.add_entry()."""
        data = [[1,2,3],[4,5,6],[7,8,9]]
        mdts = MultiDimensionalTimeSeries(3)

        for entry in data:
            mdts.add_entry(len(mdts), entry)

        assert len(data) == len(mdts)
        
        for idx in xrange(len(data)):
            assert [idx] + data[idx] == mdts[idx]

    def add_entry_format_test(self):
        """Test MultiDimensionalTimeSeries.add_entry with string timestamps."""
        mdts = MultiDimensionalTimeSeries(1)
        mdts.set_timeformat("%Y-%m-%d_%H:%M:%S")
        mdts.add_entry("2013-01-15_16:25:00", 42)
        mdts.add_entry("2013-01-15_16:25:00", [42])

    def timeseries_sorted_test(self):
        """Test the sorted_timeseries function."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = MultiDimensionalTimeSeries(1).from_twodim_list(data)
        
        tsTwo = tsOne.sorted_timeseries()

        assert (tsOne == tsTwo)

        tsThree = tsOne.sorted_timeseries(False)

        assert tsOne == tsThree
        assert tsTwo == tsThree

    def equal_test(self):
        """Test the == operator for TimeSeries instances."""
        data  = [[0.0, [0.0]], [0.1, [0.1]], [0.2, [0.2]], [0.3, [0.3]], [0.4, [0.4]], [0.5, [0.5]]]
        data2Dim  = [[0.0, [0.0, 0.42]], [0.1, [0.1, 0.42]], [0.2, [0.2, 0.42]], [0.3, [0.3, 0.42]], [0.4, [0.4, 0.42]], [0.5, [0.5, 0.42]]]
        
        tsOne   = MultiDimensionalTimeSeries.from_twodim_list(data)
        tsTwo   = MultiDimensionalTimeSeries.from_twodim_list(data)
        tsThree = MultiDimensionalTimeSeries.from_twodim_list(data[:-2])
        tsFour  = MultiDimensionalTimeSeries.from_twodim_list(data)
        tsFive  = MultiDimensionalTimeSeries.from_twodim_list(data)
        tsSix   = MultiDimensionalTimeSeries.from_twodim_list(data2Dim, dimensions=2)

        tsFour[1][0] = 1.3
        tsFive[1][1] = 1.3

        assert (tsOne == tsTwo)
        assert (tsOne != tsThree)
        assert (tsTwo != tsThree) 
        assert (tsOne != tsFour)  
        assert (tsOne != tsFive)  
        assert (tsThree != tsFour)
        assert (tsThree != tsFive)
        assert (tsFour != tsFive) 
        assert (tsSix != tsOne)
        assert (tsSix != tsTwo)
        assert (tsSix != tsThree)
        assert (tsSix != tsFour)
        assert (tsSix != tsFive)

    def addition_test(self):
        """Test the addition of MultiDimensionalTimeSeries."""
        dataOne  = [[0.0, [0.0]], [0.1, [0.1]], [0.2, [0.2]], [0.3, [0.3]], [0.4, [0.4]], [0.5, [0.5]]]
        dataTwo  = [[0.0, [0.0]], [0.1, [0.1]], [0.2, [0.2]], [0.3, [0.3]], [0.4, [0.4]], [0.5, [0.5]]]
        data2Dim  = [[0.0, [0.0, 0.42]], [0.1, [0.1, 0.42]], [0.2, [0.2, 0.42]], [0.3, [0.3, 0.42]], [0.4, [0.4, 0.42]], [0.5, [0.5, 0.42]]]
        dataThree  = dataOne + dataTwo

        tsOne = MultiDimensionalTimeSeries.from_twodim_list(dataOne)
        tsTwo = MultiDimensionalTimeSeries.from_twodim_list(dataTwo)
        tsThree = MultiDimensionalTimeSeries.from_twodim_list(dataThree)
        tsFour = tsOne + tsTwo
        tsFive = MultiDimensionalTimeSeries.from_twodim_list(data2Dim, dimensions=2)

        assert tsFour == tsThree
        try:
            tsFive + tsOne
        except ValueError:
            pass    
        else:
            assert False    # pragma: no cover

    def list_serialization_formatfree_test(self):
        """Test the format free list serialization."""
        data = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = MultiDimensionalTimeSeries.from_twodim_list(data)

        data = tsOne.to_twodim_list()
        tsTwo = MultiDimensionalTimeSeries.from_twodim_list(data)

        assert tsOne == tsTwo

    def list_serialization_format_test(self):
        """Test the list serialization including time foramtting instructions."""
        data = [[0.0, 0.0], [1.0, 0.1], [2.0, 0.2], [3.0, 0.3], [4.0, 0.4], [5.0, 0.5]]
        tsOne = MultiDimensionalTimeSeries.from_twodim_list(data)

        tsOne.set_timeformat("%Y-%m-%d_%H:%M:%S")
        data = tsOne.to_twodim_list()
        tsTwo = MultiDimensionalTimeSeries.from_twodim_list(data, format="%Y-%m-%d_%H:%M:%S")

        assert tsOne == tsTwo

    def copy_test(self):
        """Test TimeSeries cloning."""
        ts = MultiDimensionalTimeSeries.from_twodim_list([[0.5, 0.0], [1.5, 1.0], [2.5, 2.0], [3.5, 3.0], [4.5, 4.0], [5.5, 5.0]])
        tsClone = copy(ts)

        assert tsClone == ts
        
        ts[0][0] = 0.0
        assert ts != tsClone

        ts.add_entry(0.0, 1.1)
        assert len(ts) > len(tsClone)

    def gnuplot_serialization_without_format_test(self):
        """Test serialization of timeSeries into gnuplot file."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = MultiDimensionalTimeSeries.from_twodim_list(data, dimensions=1)
        tsOne.to_gnuplot_datafile("temp_plot.dat")
        
        assert os.path.isfile("temp_plot.dat")

    def gnuplot_serialization_with_format_test(self):
        """Test serialization of timeSeries into gnuplot file."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = MultiDimensionalTimeSeries.from_twodim_list(data, dimensions=1)
        tsOne.set_timeformat("%Y-%m-%d_%H:%M:%S")
        tsOne.to_gnuplot_datafile("temp_plot.dat")
        
        assert os.path.isfile("temp_plot.dat")

    def gnuplot_serialization_exception_handling_test(self):
        """Test serialization of timeSeries into gnuplot file."""
        data  = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        tsOne = MultiDimensionalTimeSeries.from_twodim_list(data, dimensions=1)
        tsOne.to_gnuplot_datafile(None)

    def normalize_test(self):
        """This is an empty test."""
        try:
            MultiDimensionalTimeSeries(3).normalize()
        except NotImplementedError:
            pass    # pragma: no cover
        else:
            assert False    # pragma: no cover
