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
from pycast.errors.baseerrormeasure import BaseErrorMeasure
from pycast.common.timeseries import TimeSeries

class BaseErrorMeasureTest(unittest.TestCase):
    """Test class for the BaseErrorMeasure interface."""

    def initialization_test(self):
        """Test the BaseErrorMeasure initialization."""
        bem = BaseErrorMeasure()

    def get_error_test(self):
        """Test the get_error of BaseErrorMeasure."""
        bem = BaseErrorMeasure()

        if not None == bem.get_error(): raise AssertionError

        bem._error = 3
        if not bem._error == 3:         raise AssertionError

    def calculate_test(self):
        """Test if calculate throws an error as expected."""
        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg  = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        try:
            bem.calculate(tsOrg, tsCalc)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

    def lower_than_test(self):
        """Test __lt__ for BaseErrorMeasure."""
        bemOne  = BaseErrorMeasure()
        bemTwo  = BaseErrorMeasure()
        bemNone = None

        bemOne._error = 0
        bemTwo._error = 1

        if not bemOne < bemTwo: raise AssertionError

        try:
            result = bemOne < None
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        
