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
from pycast.errors.medianabsolutepercentageerror import MedianAbsolutePercentageError
from pycast.common.timeseries import TimeSeries

class MedianAbsolutePercentageErrorTest(unittest.TestCase):

    def setUp(self):
        self.dataOrg = [1.0,    2.3,    0.1,    -2.0,   -1.0,   0.0,    -0.2,   -0.3,   0.15,   -0.2,   0]
        self.dataCalc = [1.2,   2.0,    -0.3,   -1.5,   -1.5,   0.3,    0.0,    0.3,    -0.15,  0.3,   0]
        # localErrors:   20     13.04   400     25      50      NA      100     200     200     250     NA

    def error_calculation_test(self):
        """ Test error calculation for MedianAbsolutePercentageError"""
        mdape = MedianAbsolutePercentageError()

        tsOrg  = TimeSeries()
        tsCalc = TimeSeries()

        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx),  self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        mdape.initialize(tsOrg, tsCalc)

        self.assertEqual(mdape.get_error(), 100)
        self.assertEqual(mdape.get_error(20.0, 50.0), 50)



#    def error_calculation_test(self):
#        """Test the MdAPE error calculation."""
#        dataOrg         = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,8], [7.3, 5], [8, 0], [9,10]]
#        dataCalc        = [[1,3], [2,5], [3,0], [4,3], [5,5], [6.1,6], [7,3], [7.3, 5], [8, 0], [9,9]]
#                           200    150    100    25      0       NA      62.5    0         NA     10
#
#        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
#        tsCalc = TimeSeries.from_twodim_list(dataCalc)
#
#        em = MedianAbsolutePercentageError()
#        em.initialize(tsOrg, tsCalc)
#
#        assert em.get_error() == 62.5
#        assert em.get_error(20.0, 50.0) == 100.0
