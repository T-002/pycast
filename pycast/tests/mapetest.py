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
from pycast.errors import MeanAbsolutePercentageError, GeometricMeanAbsolutePercentageError

class MeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Test class containing all tests for MeanAbsolutePercentageError."""
    def local_error_test(self):
        mape = MeanAbsolutePercentageError()

        try:
            mape.local_error(1, 1)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

    def error_calculation_test(self):
        """Test the calculation of the MeanAbsolutePercentageError."""
        mape = MeanAbsolutePercentageError()

        mape.initialize(TimeSeries(), TimeSeries())

        try:
            mape.get_error()
        except StandardError:
            pass
        else:
            assert False    # pragma: no cover

        ## This can be removed, after the error measure is implemented
        try:
            mape.calculate(0.0, 100.0)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

class GeometricMeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Test class containing all tests for GeometricMeanAbsolutePercentageError."""
    def local_error_test(self):
        gmape = GeometricMeanAbsolutePercentageError()

        try:
            gmape.local_error(1, 1)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

    def error_calculation_test(self):
        """Test the calculation of the GeometricMeanAbsolutePercentageError."""
        gmape = GeometricMeanAbsolutePercentageError()

        gmape.initialize(TimeSeries(), TimeSeries())

        try:
            gmape.get_error()
        except StandardError:
            pass
        else:
            assert False    # pragma: no cover

        ## This can be removed, after the error measure is implemented
        try:
            gmape.calculate(0.0, 100.0)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover
