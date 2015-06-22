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

# required external modules
import unittest

# required modules from pycast
from pycast.common.timeseries import TimeSeries
from pycast.errors.geometricmeanabsolutepercentageerror import GeometricMeanAbsolutePercentageError
import math

class GeometricMeanAbsolutePercentageErrorTest(unittest.TestCase):

    """Test class containing all tests for GeometricMeanAbsolutePercentageError."""

    def local_error_test(self):
        orgValues = [11, 33.1, 2.3, 6.54, 123.1, 12.54, 12.9]
        calValues = [24, 1.23, 342, 1.21, 4.112, 9.543, 3.54]

        gmape = GeometricMeanAbsolutePercentageError()
        for idx in xrange(len(orgValues)):
            res = ((math.fabs(calValues[idx] - orgValues[idx]))/orgValues[idx])*100
            assert  str(res)[:6] == str(gmape.local_error([orgValues[idx]], [calValues[idx]]))[:6]

    def error_calculation_test(self):
        """Test the calculation of the GeometricMeanAbsolutePercentageError."""
        dataOrg         = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,8], [7.3, 5], [8, 0], [9,10]]
        dataCalc        = [[1,3], [2,5], [3,0], [4,3], [5,6], [6.1,6], [7,3], [7.3, 5], [8, 0], [9,9]]
        # abs difference:     2      3      3      1      1       NA      5    0         NA       1
        # local errors:       200    150    100    25     20       NA     62,5 0         NA       10
        # product: 937500000000

        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        gmape = GeometricMeanAbsolutePercentageError()
        gmape.initialize(tsOrg, tsCalc)
        assert str(gmape.get_error())[:6] == "31.368"

        error = gmape.get_error(startDate=1, endDate=9)
        assert str(error)[:6] == "31.368", "%s != 31.368" % error
