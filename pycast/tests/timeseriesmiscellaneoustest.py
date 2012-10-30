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
import unittest, re

## required modules from pycast
from pycast.common.timeseries import TimeSeries

class TimeSeriesMiscellaneousTest(unittest.TestCase):
    """Test class containing tests for miscallaneous TimeSeries functions."""

    def setUp(self):
        """Initializes the environment for each test."""

    def tearDown(self):
        """This function gets called after each test function."""

    def validity_of___str___test(self):
        """Test the validity of __str__ for a given TimeSeries."""
        ts = TimeSeries()
        ts.add_entry(0.0, 0.0)
        ts.add_entry(0.1, 0.1)
        ts.add_entry(0.2, 0.2)
        ts.add_entry(0.3, 0.3)
        ts.add_entry(0.4, 0.4)

        matchres = re.match("TimeSeries\(\[(.*)\]\)", ts.__str__())
        
        assert None != matchres
        assert matchres

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

        assert len(tsOrg) == len(tsNew)
        assert tsOrg == tsNew


    def json_serialization_format_test(self):
        """Test the json serialialization with predefined format."""
        tsOrg = TimeSeries()
        tsOrg.add_entry(0.0, 0.0)
        tsOrg.add_entry(1.0, 0.1)
        tsOrg.add_entry(2.0, 0.2)
        tsOrg.add_entry(3.0, 0.3)
        tsOrg.add_entry(4.0, 0.4)
        json = tsOrg.to_json(format="%Y-%m-%d_%H:%M:%S")

        tsNew = TimeSeries.from_json(json, format="%Y-%m-%d_%H:%M:%S")

        assert len(tsOrg) == len(tsNew)
        assert tsOrg == tsNew

    def list_initialization_test(self):
        """Test TimeSeries initialization from a given list."""
        data = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]

        tsOne = TimeSeries()
        for entry in data:
            tsOne.add_entry(*entry)

        tsTwo = TimeSeries.from_twodim_list(data)

        assert len(tsOne) == len(tsTwo)
        assert tsOne == tsTwo