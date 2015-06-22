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
from pycast.errors.meanabsolutepercentageerror import MeanAbsolutePercentageError

class MeanAbsolutePercentageErrorTest(unittest.TestCase):

    """Test class containing all tests for MeanAbsolutePercentageError."""

    def setUp(self):
        self.dataOrg = [1.0,    2.3,    0.1,    -2.0,   -1.0,   0.0,    -0.2,   -0.3,   0.15,   -0.2,   0]
        self.dataCalc = [1.2,   2.0,    -0.3,   -1.5,   -1.5,   0.3,    0.0,    0.3,    -0.15,  0.3,   0]

    def tearDown(self):
        pass

    def local_error_test(self):
        """Test MeanAbsolutePercentageError.local_error."""
        localErrors = [20,  13.043, 400,  25, 50,    None,  100,  200,  200,  250, None]

        mape = MeanAbsolutePercentageError()

        for i in xrange(len(self.dataOrg)):
            calc_local_error = mape.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            if calc_local_error:
                self.assertEquals("%.3f" % calc_local_error,"%.3f" % localErrors[i])
            else:
                self.assertEquals(localErrors[i], None)

    def error_calculation_test(self):
        """Test the calculation of the MeanAbsolutePercentageError."""
        tsOrg  = TimeSeries()
        tsCalc = TimeSeries()

        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx),  self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        mape = MeanAbsolutePercentageError()
        mape.initialize(tsOrg, tsCalc)

        self.assertEquals("139.78", str(mape.get_error())[:6])


#    def local_error_test(self):
#        orgValues = [11, 33.1, 2.3, 6.54, 123.1, 12.54, 12.9]
#        calValues = [24, 1.23, 342, 1.21, 4.112, 9.543, 3.54]
#
#        mape = MeanAbsolutePercentageError()
#        for idx in xrange(len(orgValues)):
#            res = ((math.fabs(calValues[idx] - orgValues[idx]))/orgValues[idx])*100
#            assert  str(res)[:6] == str(mape.local_error([orgValues[idx]], [calValues[idx]]))[:6]
#
#    def error_calculation_test(self):
#        """Test the calculation of the MeanAbsolutePercentageError."""
#        dataOrg         = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,8], [7.3, 5], [8, 0], [9,10], [10, -10]]
#        dataCalc        = [[1,3], [2,5], [3,0], [4,3], [5,5], [6.1,6], [7,3], [7.3, 5], [8, 0], [9,9], [10, -15]]
#        # abs difference:     2      3      3      1      0       NA      5    0         NA       1         5
#        # local errors:       200    150    100    25     0       NA      62,5 0         NA       10        50
#        # sum: 597,5
#
#        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
#        tsCalc = TimeSeries.from_twodim_list(dataCalc)
#
#        mape = MeanAbsolutePercentageError()
#        mape.initialize(tsOrg, tsCalc)
#        assert str(mape.get_error())[:6] == "66.388"
