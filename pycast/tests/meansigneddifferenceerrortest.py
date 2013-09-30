#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Copyright (c) 2012-2013 Christian Schwarz
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
from pycast.errors import MeanSignedDifferenceError
from pycast.common.timeseries import TimeSeries


class MeanSignedDifferenceErrorTest(unittest.TestCase):
    """Test for the MeanSignedDifferenceError."""

    def setUp(self):
        self.dataOrg = [1.0,    2.3,    0.1,    -2.0,   -1.0,   0.0,    -0.2,   -0.3,   0.15,   -0.2,   0]
        self.dataCalc = [1.2,   2.0,    -0.3,   -1.5,   -1.5,   0.3,    0.0,    0.3,    -0.15,  0.3,   0]

    def local_error_test(self):
        """Test MeanSignedDifferenceError.local_error."""
        localErrors = [0.2,	-0.3, -0.4, 0.5, -0.5, 0.3, 0.2, 0.6, -0.3, 0.5, 0]

        msd = MeanSignedDifferenceError()

        for i in xrange(len(self.dataOrg)):
            calc_local_error = msd.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            self.assertEquals("%.4f" % calc_local_error,"%.4f" % localErrors[i])


    def error_calculation_test(self):

        msd = MeanSignedDifferenceError()

        tsOrg  = TimeSeries()
        tsCalc = TimeSeries()

        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx),  self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        msd.initialize(tsOrg, tsCalc)

        self.assertEquals(str(msd.get_error())[:6], 0.7272)

#    def setUp(self):
#        self.ts1 = TimeSeries.from_twodim_list([[1.0, 1.0], [2.0,20.0], [3.0, 3.0], [4.0, 15.0]])
#        self.ts2 = TimeSeries.from_twodim_list([[1.0,10.0], [2.0, 2.0], [3.0,30.0], [4.0, 5.0]])
#        self.msd = MeanSignedDifferenceError()
#        self.msd.initialize(self.ts1, self.ts2)
#
#    def local_error_test(self):
#        self.assertEquals(-10, self.msd.local_error(10, 20))
#        self.assertEquals(10, self.msd.local_error(20, 10))
#
#    def error_calculation_test(self):
#        self.assertEquals(self.msd.get_error(), -2)
#
#    def confidence_interval_test(self):
#        self.assertRaises(ValueError, self.msd.confidence_interval, 2)
#        self.assertEquals((-9, 10), self.msd.confidence_interval(.5))
