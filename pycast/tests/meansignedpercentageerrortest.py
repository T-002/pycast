#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Copyright (c) 2012-2015 Christian Schwarz
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
from pycast.errors import MeanSignedPercentageError
import math


class MeanSignedPercentageErrorTest(unittest.TestCase):
    """Test class containing all tests for MeanSignedPercentageError."""


    def setUp(self):
        self.dataOrg = [1.0,    2.3,    0.1,    -2.0,   -1.0,   0.0,    -0.2,   -0.3,   0.15,   -0.2,   0]
        self.dataCalc = [1.2,   2.0,    -0.3,   -1.5,   -1.5,   0.3,    0.0,    0.3,    -0.15,  0.3,   0]

    def tearDown(self):
        pass

    def local_error_test(self):
        """Test MeanSignedPercentageError.local_error."""
        localErrors = [20,  -13.043, -400,  -25, 50,    None,  -100,  -200,  -200,  -250, None]

        mpe = MeanSignedPercentageError()

        for i in xrange(len(self.dataOrg)):
            calc_local_error = mpe.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            if calc_local_error:
                self.assertEquals("%.3f" % calc_local_error,"%.3f" % localErrors[i])
            else:
                self.assertEquals(localErrors[i], None)

#    def local_error_test(self):
#        orgValues = [11, 33.1, 2.3, 6.54, 123.1, 12.54, 12.9, 0, -10]
#        calValues = [24, 1.23, 342, 1.21, 4.112, 9.543, 3.54, -1, -5]

#        mspe = MeanSignedPercentageError()
#        for idx in xrange(len(orgValues)):
#            res = (float(calValues[idx] - orgValues[idx])/orgValues[idx])*100 if orgValues[idx] else None
#            self.assertEqual(str(res)[:6], str(mspe.local_error([orgValues[idx]], [calValues[idx]]))[:6])
