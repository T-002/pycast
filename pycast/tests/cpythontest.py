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
import unittest

## required modules from pycast
from pycast.common.timeseries import TimeSeries
from pycast.common import PyCastObject
from pycast.errors import BaseErrorMeasure

class CPythonErrorMeasureTest(unittest.TestCase):
    """ Test the part of error measures that is implemented as a C extension"""
    def setUp(self):
        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        self.aTimesSerie = TimeSeries.from_twodim_list(data)
        self.anotherTimeSeries = TimeSeries.from_twodim_list(data)

        PyCastObject.enable_global_optimization()

    def tearDown(self):
        PyCastObject.disable_global_optimization()

    def optimization_enablement_test(self):
        """Test for optimization enablement."""
        em = BaseErrorMeasure()
        em._enable_instance_optimization()
        em._disable_instance_optimization()

    def initialize_test(self):
        errorMeasure = BaseErrorMeasure()
        print errorMeasure.initialize(self.aTimesSerie, self.anotherTimeSeries)
