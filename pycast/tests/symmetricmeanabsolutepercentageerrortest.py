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
from pycast.errors.symmetricmeanabsolutepercentageerror import SymmetricMeanAbsolutePercentageError
from pycast.common.timeseries import TimeSeries


class SymmetricMeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Testing symmetric mean absolute percentage error."""

    def setUp(self):
        self.dataOrg = [1.0,    2.3,    0.1,    -2.0,   -1.0,   0.0,    -0.2,   -0.3,   0.15,   -0.2,   0]
        self.dataCalc = [1.2,   2.0,    -0.3,   -1.5,   -1.5,   0.3,    0.0,    0.3,    -0.15,  0.3,   0]

    def tearDown(self):
        pass

    def local_error_test(self):
        """Test SymmetricMeanAbsolutePercentageError.local_error."""
        localErrors = [18.182,  13.953, 200,  28.571, 40,    200,  200,  200,  200,  200, 0]

        smape = SymmetricMeanAbsolutePercentageError()

        for i in xrange(len(self.dataOrg)):
            calc_local_error = smape.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            self.assertEquals("%.3f" % calc_local_error,"%.3f" % localErrors[i])

    def error_calculation_test(self):
        """Test the calculation of the SymmetricMeanAbsolutePercentageError."""
        tsOrg  = TimeSeries()
        tsCalc = TimeSeries()
        
        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx),  self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        smape = SymmetricMeanAbsolutePercentageError()
        smape.initialize(tsOrg, tsCalc)

        self.assertEquals("118.24", str(smape.get_error())[:6])

#    def local_error_test(self):
#        """Test SymmetricMeanAbsolutePercentageError local error."""
#        dataPtsOrg  = [2.30,     .373,           .583,          1.88,  1.44,         -0.0852, -.341,  .619,  .131,  1.27, 4.0]
#        dataPtsCalc = [-1.21,   -.445,           .466,          .226, -.694,           -.575,  2.73, -1.49, -1.45, -.193, 4.0]
#        localErrors = [  2.0,     2.0, 0.223069590086, 1.57075023742,   2.0,   1.48379279006,   2.0,   2.0,   2.0,   2.0, 0.0]
#
#        smape = SymmetricMeanAbsolutePercentageError()
#
#        for idx in xrange(len(dataPtsOrg)):
#            le = smape.local_error([dataPtsOrg[idx]], [dataPtsCalc[idx]])
#            ple = localErrors[idx]
#
#            ## compare the strings due to accuracy
#            assert str(le) == str(ple)

#    def error_calculation_test(self):
#        """Test the calculation of the SymmetricMeanAbsolutePercentageError."""
#        dataPtsOrg  = [2.30,     .373,           .583,          1.88,  1.44,         -0.0852, -.341,  .619,  .131,  1.27, 0]
#        dataPtsCalc = [-1.21,   -.445,           .466,          .226, -.694,           -.575,  2.73, -1.49, -1.45, -.193, 0]
#
#        tsOrg  = TimeSeries()
#        tsCalc = TimeSeries()
#        
#        for idx in xrange(len(dataPtsOrg)):
#            tsOrg.add_entry(float(idx),  dataPtsOrg[idx])
#            tsCalc.add_entry(float(idx), dataPtsCalc[idx])
#
#        smape = SymmetricMeanAbsolutePercentageError()
#        smape.initialize(tsOrg, tsCalc)
#        print smape._errorValues
#
#        ## compare the strings due to accuracy
#        assert "1.5706" == str(smape.get_error())[:6]

#    def confidence_interval_test(self):
#        """Test for None values in BaseErrorMeasure.confidence_interval"""  
#        dataPtsOrg  = [2.30,     .373,           .583,          1.88,  1.44,         -0.0852, -.341,  .619,  .131,  1.27, 0]
#        dataPtsCalc = [-1.21,   -.445,           .466,          .226, -.694,           -.575,  2.73, -1.49, -1.45, -.193, 0]
#
#        tsOrg  = TimeSeries()
#        tsCalc = TimeSeries()
#        
#        for idx in xrange(len(dataPtsOrg)):
#            tsOrg.add_entry(float(idx),  dataPtsOrg[idx])
#            tsCalc.add_entry(float(idx), dataPtsCalc[idx])
#
#        smape = SymmetricMeanAbsolutePercentageError()
#        smape.initialize(tsOrg, tsCalc)
#
#        print smape._errorValues 
#
#        self.assertEquals((0.0, 2.0), smape.confidence_interval(.5))
