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
from pycast.errors import BaseErrorMeasure
from pycast.errors import MeanSquaredError
from pycast.common.timeseries import TimeSeries

class BaseErrorMeasureTest(unittest.TestCase):
    """Test class for the BaseErrorMeasure interface."""

    def initialization_test(self):
        """Test the BaseErrorMeasure initialization."""
        bem = BaseErrorMeasure()

        for percentage in [-1.2, -0.1, 100.1, 123.9]:
            try:
                bem = BaseErrorMeasure(percentage)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

        for percentage in [0.0, 12.3, 53.4, 100.0]:
            try:
                bem = BaseErrorMeasure(percentage)
            except ValueError:    # pragma: no cover
                assert False      # pragma: no cover

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

    def local_error_test(self):
        """Test local_error of BaseErrorMeasure."""
        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg  = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        for idx in xrange(len(tsOrg)):
            try:
                bem.local_error(tsOrg[idx][1], tsCalc[idx][1])
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

class MeanSquaredErrorTest(unittest.TestCase):
    """Testing MeanSquaredError."""

    def local_error_test(self):
        """Test the local error of MeanSquaredError."""
        orgValues = [11, 33.1, 2.3, 6.54, 123.1, 12.54, 12.9]
        calValues = [24, 1.23, 342, 1.21, 4.112, 9.543, 3.54]

        mse = MeanSquaredError()
        for idx in xrange(len(orgValues)):
            res = (calValues[idx] - orgValues[idx])**2
            assert  res == mse.local_error(orgValues[idx], calValues[idx])

    def number_of_comparisons_test(self):
        """Test MeanSquaredError for a valid response to the minimalErrorCalculationPercentage."""
        dataOrg  = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9]]
        dataCalc = [[0,0],[1,1],[2,2],[3,3],[4,4],[5.1,5],[6.1,6],[7.1,7],[8.1,8],[9.1,9]]

        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        mse = MeanSquaredError(60.0)

        ## only 50% of the original TimeSeries have a corresponding partner
        if mse.calculate(tsOrg, tsCalc):
            assert False    # pragma: no cover

        if not mse.calculate(tsOrg, tsOrg):
            assert False    # pragma: no cover

    def error_calculation_test(self):
        """Test for a valid error calculation."""
        dataOrg         = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,  6], [7,7], [8,8],   [9,9]]
        dataCalc        = [[0,1], [1,3], [2,5], [3,0], [4,3], [5,5], [6.1,6], [7,3], [8.1,8], [9,8]]
        # difference:         1      2      3      3      1      0       NA      4       NA      1
        # local errors:       1      4      9      9      1      0       NA     16       NA      1

        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        mse = MeanSquaredError(80.0)
        assert mse.get_error() == None

        mse.calculate(tsOrg, tsCalc)

        assert mse.get_error() == 5.125