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
from pycast.errors            import SymmetricMeanAbsolutePercentageError as SMAPE
from pycast.common.timeseries import TimeSeries
from pycast.methods           import BaseForecastingMethod

from pycast.optimization import GridSearch

class GridSearchTest(unittest.TestCase):
    """Test class for the GridSearch."""

    def setUp(self):
        """Initializes self.forecastingMethod."""
        bfm = BaseForecastingMethod(["parameter_one", "parameter_two"])
        bfm._parameterIntervals = {}
        bfm._parameterIntervals["parameter_one"] = [0.0, 1.0, False, False]
        bfm._parameterIntervals["parameter_two"] = [0.0, 2.0, True, True]

        self.bfm = bfm
        data = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]]
        self.timeSeries = TimeSeries.from_twodim_list(data)

    def tearDown(self):
        """Deletes the BaseForecastingMethod of the test."""
        del self.bfm
        del self.timeSeries

    def create_generator_test(self):
        """Test the parameter generation function."""
        ## initialize a correct result
        precision = 10**-2
        values_one = [i * precision for i in xrange(1,100)]
        values_two = [i * precision for i in xrange(201)]

        generator_one = GridSearch(SMAPE, -2)._generate_next_parameter_value("parameter_one", self.bfm)
        generator_two = GridSearch(SMAPE, -2)._generate_next_parameter_value("parameter_two", self.bfm)

        generated_one = [val for val in generator_one]
        generated_two = [val for val in generator_two]

        assert len(values_one) == len(generated_one)
        assert len(values_two) == len(generated_two)

        for idx in xrange(len(values_one)):
            value = str(values_one[idx])[:12]
            assert str(value) == str(generated_one[idx])[:len(value)]

        for idx in xrange(len(values_two)):
            value = str(values_two[idx])[:12]
            assert str(value) == str(generated_two[idx])[:len(value)]

    def optimize_exception_test(self):
        """Test for exception while calling GridSearch.optimize."""
        try:
            GridSearch(SMAPE, -2).optimize(self.timeSeries)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        GridSearch(SMAPE, -2).optimize(self.timeSeries, [BaseForecastingMethod()])



