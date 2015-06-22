# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# Copyright (c) 2012-2015 Christian Schwarz
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## required external modules
import unittest

## required modules from pycast
from pycast.errors.weightedmeanabsolutepercentageerror import WeightedMeanAbsolutePercentageError
from pycast.common.timeseries import TimeSeries

class WeightedMeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Test class containing all tests for WeightedMeanAbsolutePercentageError."""
    def local_error_test(self):
        orgValues = [11, 33.1, 2.3, 6.54, 123.1, 12.54, 12.9]
        calValues = [24, 1.23, 342, 1.21, 4.112, 9.543, 3.54]
        resValues = ['118.181', '192.567', '14769.5', '162.996', '193.319', '47.7990', '145.116']

        wmape = WeightedMeanAbsolutePercentageError()
        for idx in xrange(len(orgValues)):
            localError = wmape.local_error([orgValues[idx]], [calValues[idx]])
            assert str(resValues[idx]) == str(localError)[:7], str(resValues[idx]) + '!=' + str(localError)[:7]

    def error_calculation_test(self):
        """Test the calculation of the MeanAbsolutePercentageError."""
        dataOrg         = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,8], [7.3, 5], [8, 0], [9,10]]
        dataCalc        = [[1,3], [2,5], [3,0], [4,3], [5,5], [6.1,6], [7,3], [7.3, 5], [8, 0], [9,9]]
        # abs difference:     2      3      3      1      0       NA      5    0         NA       1
        # local errors:       200    150    200    50     0       NA      125  0         NA       20
        # sum: 745

        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        wmape = WeightedMeanAbsolutePercentageError()
        wmape.initialize(tsOrg, tsCalc)
        assert str(wmape.get_error())[:6] == "93.125"
