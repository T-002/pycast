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

from pycast.optimization.baseoptimizationmethod import BaseOptimizationMethod
from pycast.methods.basemethod import BaseMethod
from pycast.errors.baseerrormeasure import BaseErrorMeasure
from pycast.common.timeseries import TimeSeries

class BaseOptimizationMethodTest(unittest.TestCase):

    """Test class containing all tests for pycast.optimization.BaseOptimizationMethod."""

    def initialization_errormeasure_test(self):
        """Test optimization methods error measure initialization."""
        BaseOptimizationMethod(BaseErrorMeasure, -1)

        try:
            BaseOptimizationMethod(None, -1)
        except TypeError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            BaseOptimizationMethod(BaseOptimizationMethodTest, -1)
        except TypeError:
            pass
        else:
            assert False    # pragma: no cover

    def initialization_precision_test(self):
        """Test the parameter range durign the initialization."""
        for precision in xrange(-7, 1, 1):
            BaseOptimizationMethod(BaseErrorMeasure, precision=precision)

        for precision in [-1020, -324, -11, 1, 42, 123, 2341]:
            try:
                BaseOptimizationMethod(BaseErrorMeasure, precision=precision)
            except ValueError:
                pass
            else:
                #print "precision: %s" % precision    # pragma: no cover
                assert False                         # pragma: no cover

    def optimize_value_error_test(self):
        """Test the optimize call."""
        bom = BaseOptimizationMethod(BaseErrorMeasure, precision=-3)
        bm  = BaseMethod()

        bom.optimize(TimeSeries(), [bm])

        try:
            bom.optimize(TimeSeries(), [])
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover
