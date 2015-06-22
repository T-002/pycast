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
from pycast.errors.meanabsolutedeviationerror import MeanAbsoluteDeviationError
from pycast.common.timeseries import TimeSeries


class MeanAbsoluteDeviationErrorTest(unittest.TestCase):

    """Testing Mean Absolute Deviation error."""


    def setUp(self):
        self.dataOrg = [1.0,    2.3,    0.1,    -2.0,   -1.0,   0.0,    -0.2,   -0.3,   0.15,   -0.2,   0]
        self.dataCalc = [1.2,   2.0,    -0.3,   -1.5,   -1.5,   0.3,    0.0,    0.3,    -0.15,  0.3,   0]

    def local_error_test(self):
        """Test MeanAbsoluteDeviationError.local_error."""

        localErrors = [0.2, 0.3, 0.4, 0.5, 0.5, 0.3, 0.2, 0.6, 0.3, 0.5, 0]
#        dataPtsOrg  = [ 2.30,  .373, .583, 1.880, 500]
#        dataPtsCalc = [-1.21, -.445, .466,  .226, 300]
#        localErrors = [ 3.51,  .818, .117, 1.654, 200]

        mad = MeanAbsoluteDeviationError()

        for idx in xrange(len(self.dataOrg)):
            le = mad.local_error([self.dataOrg[idx]], [self.dataCalc[idx]])
            ple = localErrors[idx]

            # compare the strings due to accuracy
            self.assertEqual(str(le), str(ple))

    def error_calculation_test(self):
        """Test the calculation of the Mean Absolute Deviation Error."""
        #dataPtsOrg  = [2.30,     .373,           .583,          1.88,  1.44,         -0.0852, -.341,  .619,  .131,  1.27, 0]
        #dataPtsCalc = [-1.21,   -.445,           .466,          .226, -.694,           -.575,  2.73, -1.49, -1.45, -.193, 0]

        tsOrg  = TimeSeries()
        tsCalc = TimeSeries()

        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx),  self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        mad = MeanAbsoluteDeviationError()
        mad.initialize(tsOrg, tsCalc)

        # compare the strings due to accuracy
        self.assertEqual("0.3454", str(mad.get_error())[:6])
