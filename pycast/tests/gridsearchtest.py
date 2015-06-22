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
from pycast.errors.symmetricmeanabsolutepercentageerror import SymmetricMeanAbsolutePercentageError as SMAPE
from pycast.common.timeseries import TimeSeries
from pycast.methods.basemethod           import BaseForecastingMethod
from pycast.methods.exponentialsmoothing import ExponentialSmoothing, HoltMethod

from pycast.optimization.gridsearch import GridSearch

class GridSearchTest(unittest.TestCase):

    """Test class for the GridSearch."""

    def setUp(self):
        """Initializes self.forecastingMethod."""
        bfm = BaseForecastingMethod(["parameter_one", "parameter_two"])
        bfm._parameterIntervals = {}
        bfm._parameterIntervals["parameter_one"] = [0.0, 1.0, False, False]
        bfm._parameterIntervals["parameter_two"] = [0.0, 2.0, True, True]

        self.bfm = bfm
        data = [[0.0, 0.0], [1.1, 0.2], [2.2, 0.6], [3.3, 0.2], [4.4, 0.3], [5.5, 0.5]]
        self.timeSeries = TimeSeries.from_twodim_list(data)
        self.timeSeries.normalize("second")

    def tearDown(self):
        """Deletes the BaseForecastingMethod of the test."""
        del self.bfm
        del self.timeSeries

    def create_generator_test(self):
        """Test the parameter generation function."""
        # initialize a correct result
        precision = 10**-2
        values_one = [i * precision for i in xrange(1,100)]
        values_two = [i * precision for i in xrange(201)]

        generator_one = GridSearch(SMAPE, precision=-2)._generate_next_parameter_value("parameter_one", self.bfm)
        generator_two = GridSearch(SMAPE, precision=-2)._generate_next_parameter_value("parameter_two", self.bfm)

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

        try:
            GridSearch(SMAPE, -1).optimize(self.timeSeries, [self.bfm])
        # we looped down to the NotImplemetedError of BaseMethod.execute
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

    def optimize_value_creation_test(self):
        """Testing the first part of optimize_forecasting_method."""
        self.bfm._requiredParameters = ["param1", "param2", "param3", "param4", "param5"]

        try:
            GridSearch(SMAPE, -1).optimize_forecasting_method(self.timeSeries, self.bfm)
        # we looped down to the NotImplemetedError of BaseMethod.execute
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

        self.bfm._parameterIntervals = {
            "param3": [0.0, 1.0, True, True],
            "param4": [0.0, 1.0, True, True],
            "param5": [0.0, 1.0, True, True]
        }

        try:
            GridSearch(SMAPE, -5).optimize_forecasting_method(self.timeSeries, self.bfm)
        # we looped down to the NotImplemetedError of BaseMethod.execute
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

    def inner_optimization_result_test(self):
        """Test for the correct result of a GridSearch optimization."""
        fm = ExponentialSmoothing()
        startingPercentage =   0.0
        endPercentage      = 100.0

        # manually select the best alpha
        self.timeSeries.normalize("second")
        results = []
        for smoothingFactor in [alpha / 100.0 for alpha in xrange(1, 100)]:    # pragma: no cover
            fm.set_parameter("smoothingFactor", smoothingFactor)
            resultTS = self.timeSeries.apply(fm)
            error = SMAPE()
            error.initialize(self.timeSeries, resultTS)
            results.append([error, smoothingFactor])

        bestManualResult = min(results, key=lambda item: item[0].get_error(startingPercentage, endPercentage))

        # Debugging
        #print ""
        #for item in results:
        #    print "Manual: %s / %s" % (str(item[0].get_error(startingPercentage, endPercentage))[:8], item[1])
        #print ""

        # automatically determine the best alpha using GridSearch
        gridSearch = GridSearch(SMAPE, precision=-2)
        # used, because we test a submethod here
        gridSearch._startingPercentage = startingPercentage
        gridSearch._endPercentage      = endPercentage
        result     = gridSearch.optimize_forecasting_method(self.timeSeries, fm)

        # the grid search should have determined the same alpha
        bestManualAlpha     = bestManualResult[1]
        errorManualResult     = bestManualResult[0].get_error()

        bestGridSearchAlpha   = result[1]["smoothingFactor"]
        errorGridSearchResult = result[0].get_error()

        # Debugging
        #print ""
        #print "GridSearch Result"
        #print "Manual:     SMAPE / Alpha: %s / %s" % (str(errorManualResult)[:8],     bestManualAlpha)
        #print "GridSearch: SMAPE / Alpha: %s / %s" % (str(errorGridSearchResult)[:8], bestGridSearchAlpha)
        #print ""

        assert str(errorManualResult)[:8] >= str(errorGridSearchResult)[:8]
        assert str(bestManualAlpha)[:5] == str(bestGridSearchAlpha)[:5]

    def inner_optimization_result_accuracy_test(self):
        """Test for the correct result of a GridSearch optimization."""
        fm = ExponentialSmoothing()
        startingPercentage =   0.0
        endPercentage      = 100.0

        # manually select the best alpha
        self.timeSeries.normalize("second")
        results = []
        for smoothingFactor in [alpha / 100.0 for alpha in xrange(1, 100)]:    # pragma: no cover
            fm.set_parameter("smoothingFactor", smoothingFactor)
            resultTS = self.timeSeries.apply(fm)
            error = SMAPE()
            error.initialize(self.timeSeries, resultTS)
            results.append([error, smoothingFactor])

        bestManualResult = min(results, key=lambda item: item[0].get_error(startingPercentage, endPercentage))

        # automatically determine the best alpha using GridSearch
        gridSearch = GridSearch(SMAPE, precision=-4)

        # used, because we test a submethod here
        gridSearch._startingPercentage = startingPercentage
        gridSearch._endPercentage      = endPercentage

        result     = gridSearch.optimize_forecasting_method(self.timeSeries, fm)

        # the grid search should have determined the same alpha
        bestManualAlpha     = bestManualResult[1]
        errorManualResult     = bestManualResult[0].get_error()

        bestGridSearchAlpha   = result[1]["smoothingFactor"]
        errorGridSearchResult = result[0].get_error()

        assert errorManualResult > errorGridSearchResult

    def outer_optimization_result_test(self):
        """Test the multiple method optimization."""
        fm1 = ExponentialSmoothing()
        fm2 = HoltMethod()

        self.timeSeries.normalize("second")

        # automatically determine the best alpha using GridSearch
        gridSearch = GridSearch(SMAPE, precision=-2)
        result     = gridSearch.optimize(self.timeSeries, [fm1, fm2])

    def optimization_loop_test(self):
        """Testing the optimozation loop."""
        gridSearch = GridSearch(SMAPE, precision=-2)

        def crap_execute(ignoreMe):
            ts = self.timeSeries.to_twodim_list()
            ts = TimeSeries.from_twodim_list(ts)

            for entry in ts:
                entry[0] += 0.1

            return ts

        self.bfm.execute = crap_execute

        result = gridSearch.optimization_loop(self.timeSeries, self.bfm, [], {})
        assert result == []
