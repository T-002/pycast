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
import random

# required modules from pycast
from pycast.common.timeseries import TimeSeries
from pycast.methods.basemethod import BaseMethod, BaseForecastingMethod
from pycast.methods.simplemovingaverage import SimpleMovingAverage
from pycast.methods.exponentialsmoothing import ExponentialSmoothing, HoltMethod, HoltWintersMethod

class BaseMethodTest(unittest.TestCase):

    """Test class containing all tests for pycast.method.basemethod."""

    def initialization_test(self):
        """Test BaseMethod initialization."""
        hasToBeSorted     = random.choice([True, False])
        hasToBeNormalized = random.choice([True, False])
        b = BaseMethod(["param1", "param2"], hasToBeSorted=hasToBeSorted, hasToBeNormalized=hasToBeNormalized)

        if not b.has_to_be_sorted() == hasToBeSorted:
            raise AssertionError
        if not b.has_to_be_normalized() == hasToBeNormalized:
            raise AssertionError

    def parameter_set_test(self):
        """Test if the parameters of a method are set correctly."""
        b = BaseMethod(["param1", "param2"])
        b.set_parameter("param1", 1)
        b.set_parameter("param2", 2)
        b.set_parameter("param1", 1)

        if not len(b._parameters) == 2: raise AssertionError

    def get_parameter_intervals_exception_test(self):
        """Testing for NotImplementedError."""
        class IllegalMethodErrorClass(BaseMethod):
            pass

        try:
            IllegalMethodErrorClass()
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

    def required_parameter_test(self):
        """Test for required parameters."""
        parameters = ["param1", "param2"]

        b = BaseMethod(parameters)

        requiredParameters = b.get_required_parameters()

        for parameter in parameters:
            if not parameter in requiredParameters:
                raise AssertionError    # pragma: no cover

        assert len(parameters) == len(requiredParameters)

    def interval_validity_test(self):
        """Test if BaseMethod handles parameter validity correctly."""
        parameters = ["param1", "param2", "param3", "param4"]

        b = BaseMethod(parameters)

        # overwrite parameter validity dictionary for testing
        b._parameterIntervals = {
            "param1": [0.0, 1.0, False, False],
            "param2": [0.0, 1.0, False, True],
            "param3": [0.0, 1.0, True, False],
            "param4": [0.0, 1.0, True, True]
        }

        # definetely invalid parameters
        for value in [-1.5, 3.2]:
            for parameter in parameters:
                if b._in_valid_interval(parameter, value):
                    assert False    # pragma: no cover

        # definetly valid parameters
        for value in [0.3, 0.42]:
            for parameter in parameters:
                if not b._in_valid_interval(parameter, value):
                    assert False    # pragma: no cover

    def get_interval_test(self):
        """Test if correct intervals are returned."""
        parameters = ["param1", "param2", "param3", "param4"]

        b = BaseMethod(parameters)

        # overwrite parameter validity dictionary for testing
        parameterIntervals = {
            "param1": [0.0, 1.0, False, False],
            "param2": [0.0, 1.0, False, True],
            "param3": [0.0, 1.0, True, False],
            "param4": [0.0, 1.0, True, True]
        }
        b._parameterIntervals = parameterIntervals

        for parameter in parameters:
            i = b.get_interval(parameter)
            if not i == parameterIntervals[parameter]:
                raise AssertionError    # pragma: no cover

        assert None == b.get_interval("unknown")

    def value_error_message_test(self):
        """Test the value error message."""
        parameters = ["param1", "param2", "param3", "param4"]

        b = BaseMethod(parameters)

        # overwrite parameter validity dictionary for testing
        b._parameterIntervals = {
            "param1": [0.0, 1.0, False, False],
            "param2": [0.0, 1.0, False, True],
            "param3": [0.0, 1.0, True, False],
            "param4": [0.0, 1.0, True, True]
        }

        # Unknown parameters should return no message
        if None != b._get_value_error_message_for_invalid_prarameter("unknown", 0.0):
            assert False    # pragma: no cover

        # Known parameters should return a message
        for parameter in parameters:
            if not isinstance(b._get_value_error_message_for_invalid_prarameter(parameter, 0.4), basestring):
                assert False    # pragma: no cover

    def parameter_get_test(self):
        """Test the parameter set function."""
        b = BaseMethod()
        b.set_parameter("param1", 42.23)

        param1 = b.get_parameter("param1")
        assert param1 == 42.23

        try:
            b.get_parameter("param2")
        except KeyError:
            pass
        else:
            assert False    # pragma: no cover

    def method_completition_test(self):
        """Test if methods detect their executable state correctly."""
        b = BaseMethod(["param1", "param2"])

        if b.can_be_executed(): raise AssertionError

        b.set_parameter("param1", 1)
        if b.can_be_executed(): raise AssertionError

        b.set_parameter("param2", 2)
        if not b.can_be_executed(): raise AssertionError

    def execute_not_implemented_exception_test(self):
        """Test the correct interface of BaseMethod."""
        b = BaseMethod(["param1", "param2"])

        data  = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        ts = TimeSeries.from_twodim_list(data)
        ts.normalize("second")

        try:
            b.execute(ts)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

class BaseForecastingMethodTest(unittest.TestCase):
    """Test class for the BaseForecastingMethod."""

    def initialization_test(self):
        """Testing BaseForecastingMethod initialization."""

        class FM1(BaseForecastingMethod):
            def __init__(self):
                super(FM1, self).__init__(["valuesToForecast"])

            def _get_parameter_intervals(self):
                return {}

        class FM2(BaseForecastingMethod):
            def __init__(self):
                super(FM2, self).__init__([])

            def _get_parameter_intervals(self):
                return {}

        FM1()
        FM2()
        BaseForecastingMethod(valuesToForecast=4, hasToBeNormalized=False, hasToBeSorted=True, requiredParameters=[])
        BaseForecastingMethod(valuesToForecast=4, hasToBeNormalized=False, hasToBeSorted=True)
        BaseForecastingMethod(["valuesToForecast"])
        BaseForecastingMethod(["valuesToForecast"], valuesToForecast=1)
        BaseForecastingMethod([], hasToBeNormalized=True)

    def get_optimizable_parameters_test(self):
        """Test get optimizable parameters."""
        # Initialize parameter lists
        parameters = ["param1", "param2", "param3", "param4", "param5"]
        intervals = {
            "param3": [0.0, 1.0, True, True],
            "param4": [0.0, 1.0, True, True],
            "param5": [0.0, 1.0, True, True],
            "param6": [0.0, 1.0, True, True]
        }

        # initialize BaseForecastingMethod and set some parameter intervals
        bfm = BaseForecastingMethod(parameters, valuesToForecast=4, hasToBeNormalized=False, hasToBeSorted=True)
        bfm._parameterIntervals = intervals

        # check, if the BaseForecastingMethod returns the correct parameters
        correctResult = ["param3", "param4", "param5"]
        result = sorted(bfm.get_optimizable_parameters())
        assert correctResult == result

    def initialization_exception_test(self):
        """Test BaseForecastingMethod initialization for ValueError."""
        for valuesToForecast in xrange(-10,0):
            try:
                BaseForecastingMethod(valuesToForecast=valuesToForecast)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

    def forecast_until_test(self):
        """Testing the forecast_until function."""
        for validts in (xrange(1,100)):
            BaseForecastingMethod(["valuesToForecast"]).forecast_until(validts, tsformat=None)

        BaseForecastingMethod(["valuesToForecast"]).forecast_until("2012", tsformat="%Y")

    def calculate_values_to_forecast_exception_test(self):
        """Test for correct handling of illegal TimeSeries instances.

        @todo remove NotImplementedError Catch."""
        data = [[1.5, 152.0],[2.5, 172.8],[3.5, 195.07200000000003],[4.5, 218.30528000000004]]
        ts   = TimeSeries.from_twodim_list(data)
        ts.add_entry(3, 1343)
        bfm  = BaseForecastingMethod()

        # nothing has to be done, because forecast_until was never called
        bfm._calculate_values_to_forecast(ts)

        bfm.forecast_until(134)

        try:
            bfm._calculate_values_to_forecast(ts)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        ts.sort_timeseries()
        try:
            bfm._calculate_values_to_forecast(ts)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        ts.normalize("second")
        bfm._calculate_values_to_forecast(ts)

    def number_of_values_to_forecast_test(self):
        """Test the valid calculation of values to forecast."""
        data = [[1.5, 152.0],[2.5, 172.8],[3.5, 195.07200000000003],[4.5, 218.30528000000004]]
        ts   = TimeSeries.from_twodim_list(data)
        ts.normalize("second")

        bfm  = BaseForecastingMethod()

        bfm.forecast_until(100)
        bfm._calculate_values_to_forecast(ts)

        assert bfm.get_parameter("valuesToForecast") == 96

class SimpleMovingAverageTest(unittest.TestCase):
    """Test class for the SimpleMovingAverage method."""

    def initialization_test(self):
        """Test the initialization of the SimpleMovingAverage method."""
        sm = SimpleMovingAverage(3)

        if not sm._parameters["windowsize"] == 3:   raise AssertionError

    def initialization_exception_Test(self):
        """Test the exeptions of SimpleMovingAverage's __init__."""
        for invalidWindowSize in xrange(-5, 1):
            try:
                SimpleMovingAverage(invalidWindowSize)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

        for invalidWindowSize in xrange(2, 10, 2):
            try:
                SimpleMovingAverage(invalidWindowSize)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

    def execute_value_error_test(self):
        """Test for the ValueError in SimpleMovingAverage.execute()."""
        tsOne = TimeSeries()
        data  = [[1.5, 10.0],[2.5, 12.4],[3.5, 17.380000000000003],[4.5, 16.666],[5.5, 20.6662],[6.5, 23.46634],[7.5, 20.026438]]
        tsTwo = TimeSeries.from_twodim_list(data)

        sma = SimpleMovingAverage(3)

        tsOne.normalize("second")

        res = tsTwo.apply(sma)

        try:
            tsOne.apply(sma)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

    def execute_test(self):
        """Test the execution of SimpleMovingAverage."""
        # Initialize the source
        data  = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")

        # Initialize a correct result.
        # The numbers look a little bit odd, based on the binary translation problem
        data  = [[1.5, 0.10000000000000002],[2.5, 0.20000000000000004],[3.5, 0.3]]
        tsDst = TimeSeries.from_twodim_list(data)

        # Initialize the method
        sma = SimpleMovingAverage(3)
        res = tsSrc.apply(sma)

        #print tsSrc, res
        if not res == tsDst: raise AssertionError

class ExponentialSmoothingTest(unittest.TestCase):
    """Test class for the ExponentialSmoothing method."""

    def initialization_test(self):
        """Test the initialization of the ExponentialSmoothing method."""
        ExponentialSmoothing(0.2, 0)

        for alpha in [-42.23, -0.1, 0.0, 1.0, 1.1, 3.1, 4.2]:
            try:
                ExponentialSmoothing(alpha)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

    def smoothing_test(self):
        """Test smoothing part of ExponentialSmoothing."""
        data  = [[0, 10.0], [1, 18.0], [2, 29.0], [3, 15.0], [4, 30.0], [5, 30.0], [6, 12.0], [7, 16.0]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")

        # Initialize a correct result.
        # The numbers look a little bit odd, based on the binary translation problem
        data  = [[1.5, 10.0],[2.5, 12.4],[3.5, 17.380000000000003],[4.5, 16.666],[5.5, 20.6662],[6.5, 23.46634],[7.5, 20.026438]]
        tsDst = TimeSeries.from_twodim_list(data)

        # Initialize the method
        es = ExponentialSmoothing(0.3, 0)
        res = tsSrc.apply(es)

        if not res == tsDst: raise AssertionError

        data.append([8.5, 18.8185066])
        tsDst = TimeSeries.from_twodim_list(data)

        # Initialize the method
        es = ExponentialSmoothing(0.3)
        res = tsSrc.apply(es)

        if not res == tsDst: raise AssertionError

    def second_smoothing_test(self):
        """Test smoothing part of ExponentialSmoothing a second time."""
        data  = [[0.0, 1000], [1, 1050], [2, 1120], [3, 980], [4, 110]]
        tsSrc = TimeSeries.from_twodim_list(data)

        # Initialize a correct result.
        # The numbers look a little bit odd, based on the binary translation problem
        data  = [[1.5, 1000],[2.5, 1030],[3.5, 1084],[4.5, 1021.6]]
        tsDst = TimeSeries.from_twodim_list(data)

        # Initialize the method
        tsSrc.normalize("second")
        #print tsSrc
        es = ExponentialSmoothing(0.6, 0)
        res = tsSrc.apply(es)

        #print tsSrc, res
        if not res == tsDst: raise AssertionError

    def forecasting_test(self):
        """Test forecast part of ExponentialSmoothing."""
        data  = [[0, 10.0], [1, 18.0], [2, 29.0], [3, 15.0], [4, 30.0], [5, 30.0], [6, 12.0], [7, 16.0]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")

        es = ExponentialSmoothing(0.1, 7)
        res = tsSrc.apply(es)

        # test if the correct number of values have been forecasted
        assert len(tsSrc)  + 6 == len(res)

class HoltMethodTest(unittest.TestCase):
    """Test class for the HoltMethod method."""

    def initialization_test(self):
        """Test the initialization of the HoltMethod method."""
        HoltMethod(0.2, 0.3)

        for alpha in [-0.1, 0.45,  1.1]:
            for beta in [-1.4, 3.2]:
                try:
                    HoltMethod(alpha, beta)
                except ValueError:
                    pass
                else:
                    assert False    # pragma: no cover

    def smoothing_test(self):
        """Test smoothing part of ExponentialSmoothing."""
        data  = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")

        # Initialize a correct result.
        # The numbers look a little bit odd, based on the binary translation problem
        data  = [[1.5, 0.0],[2.5, 0.12000000000000002],[3.5, 0.24080000000000004],[4.5, 0.36099200000000004]]
        tsDst = TimeSeries.from_twodim_list(data)

        # Initialize the method
        hm = HoltMethod(0.2, 0.3, valuesToForecast=0)
        res = tsSrc.apply(hm)

        if not res == tsDst: raise AssertionError

    def second_smoothing_test(self):
        """
        Test smoothing part of HoltSmoothing.

        Data: http://analysights.wordpress.com/2010/05/20/forecast-friday-topic-double-exponential-smoothing/
        """
        data  = [[0.0, 152], [1, 176], [2, 160], [3, 192], [4, 220]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")

        # Initialize a correct result.
        # The numbers look a little bit odd, based on the binary translation problem
        data  = [[1.5, 152.0],[2.5, 172.8],[3.5, 195.07200000000003],[4.5, 218.30528000000004]]
        tsDst = TimeSeries.from_twodim_list(data)

        # Initialize the method
        hm = HoltMethod(0.2, 0.3, valuesToForecast=0)
        res = tsSrc.apply(hm)

        if not res == tsDst: raise AssertionError

    def forecasting_test(self):
        """Test forecast part of ExponentialSmoothing."""
        data  = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")

        hm = HoltMethod(0.2, 0.3, 5)
        res = tsSrc.apply(hm)

        # test if the correct number of values have been forecasted
        assert len(tsSrc) + 4 == len(res)

    def second_forecasting_test(self):
       """Test forecast part of HoltSmoothing."""
       data  = [[0.0, 152], [1, 176], [2, 160], [3, 192], [4, 220]]
       tsSrc = TimeSeries.from_twodim_list(data)
       tsSrc.normalize("second")

       hm  = HoltMethod(0.2, 0.3, 5)
       res = tsSrc.apply(hm)

       # test if the correct number of values have been forecasted
       assert len(tsSrc) + 4 == len(res)

       # Validate the first forecasted value
       assert str(res[4][1])[:8] == "241.2419"

class HoltWintersMethodTest(unittest.TestCase):
    """Test class for the HoltWintersMethod method."""

    def initialization_test(self):
        """Test the initialization of the HoltWintersMethod method."""
        HoltWintersMethod(0.2, 0.3, 0.4, 5)

        for alpha in [-0.1, 0.81, 1.1]:
            for beta in [-1.4, 0.12, 3.2]:
                for gamma in [-0.05, 1.3]:
                    try:
                        HoltWintersMethod(alpha, beta, gamma)
                    except ValueError:
                        pass
                    else:
                        assert False    # pragma: no cover

    def sanity_test(self):
        """HoltWinters should throw an Exception if applied to a Time Series shorter than the season length"""
        hwm = HoltWintersMethod(seasonLength = 2)
        data  = [[0.0, 152]]
        tsSrc = TimeSeries.from_twodim_list(data)
        try:
            tsSrc.apply(hwm)
        except ValueError:
            pass
        else:
            assert False, "HoltWinters should throw an Exception if applied to a Time Series shorter than the season length"    # pragma: no cover

    def smoothing_test(self):
        """ Test if the smoothing works correctly"""

        data = [362.0, 385.0, 432.0, 341.0, 382.0, 409.0, 498.0, 387.0, 473.0, 513.0, 582.0, 474.0, 544.0, 582.0, 681.0, 557.0, 628.0, 707.0, 773.0, 592.0, 627.0, 725.0, 854.0, 661.0]
        tsSrc = TimeSeries.from_twodim_list(zip(range(len(data)),data))
        expected = [[0.0, 362.0],[1.0, 379.93673257607463],[2.0, 376.86173719924875],[3.0, 376.0203652542205],[4.0, 408.21988583215574],[5.0, 407.16235446485433],[6.0, 430.0950666716297],[7.0, 429.89797609228435],[8.0, 489.4888959723074],[9.0, 507.8407281475308],[10.0, 506.3556647249702],[11.0, 523.9422448655133],[12.0, 556.0311543025242],[13.0, 573.6520991970604],[14.0, 590.2149136780341],[15.0, 611.8813425659495],[16.0, 637.0393967524727],[17.0, 684.6600411792656],[18.0, 675.9589298142507],[19.0, 659.0266828674846],[20.0, 644.0903317144154],[21.0, 690.4507762388047],[22.0, 735.3219292023371],[23.0, 737.9752345691215]]
        hwm = HoltWintersMethod(.7556, 0.0000001, .9837, 4, valuesToForecast=0)

        initialA_2 = hwm.computeA(2, tsSrc)
        assert  initialA_2 == 510.5, "Third initial A_2 should be 510.5, but it %d" % initialA_2

        initialTrend = hwm.initialTrendSmoothingFactors(tsSrc)
        assert initialTrend == 9.75, "Initial Trend should be 9.75 but is %d" % initialTrend

        #correctness is not proven, but will be enough for regression testing
        resTS       = tsSrc.apply(hwm)
        expectedTS  = TimeSeries.from_twodim_list(expected)

        assert len(resTS) == len(expectedTS)
        assert resTS == expectedTS, "Smoothing result not correct."

    def forecasting_test(self):
        data = [362.0, 385.0, 432.0, 341.0, 382.0, 409.0, 498.0, 387.0, 473.0, 513.0, 582.0, 474.0, 544.0, 582.0, 681.0, 557.0, 628.0, 707.0, 773.0, 592.0, 627.0, 725.0, 854.0, 661.0]
        tsSrc = TimeSeries.from_twodim_list(zip(range(len(data)),data))
        expected = [[0.0, 362.0],[1.0, 379.93673257607463],[2.0, 376.86173719924875],[3.0, 376.0203652542205],[4.0, 408.21988583215574],[5.0, 407.16235446485433],[6.0, 430.0950666716297],[7.0, 429.89797609228435],[8.0, 489.4888959723074],[9.0, 507.8407281475308],[10.0, 506.3556647249702],[11.0, 523.9422448655133],[12.0, 556.0311543025242],[13.0, 573.6520991970604],[14.0, 590.2149136780341],[15.0, 611.8813425659495],[16.0, 637.0393967524727],[17.0, 684.6600411792656],[18.0, 675.9589298142507],[19.0, 659.0266828674846],[20.0, 644.0903317144154],[21.0, 690.4507762388047],[22.0, 735.3219292023371],[23.0, 737.9752345691215],[24.0, 669.767091965978],[25.0, 737.5272444120604],[26.0, 805.3947787747426],[27.0, 902.1522777060334]]

        hwm = HoltWintersMethod(.7556, 0.0000001, .9837, 4, valuesToForecast = 4)
        res = tsSrc.apply(hwm)

        #print res
        assert len(res) == len(tsSrc) + 4
        assert res == TimeSeries.from_twodim_list(expected)


    def season_factor_initialization_test(self):
        """ Test if seasonal correction factors are initialized correctly."""

        hwm = HoltWintersMethod(seasonLength=4)
        data = [[0, 362.0], [1,385.0], [2, 432.0], [3, 341.0], [4, 382.0], [5, 409.0], [6, 498.0], [7, 387.0], [8, 473.0], [9, 513.0], [10, 582.0], [11, 474.0]]
        tsSrc = TimeSeries.from_twodim_list(data)
        seasonValues = hwm.initSeasonFactors(tsSrc)

        #correctness is not proven, but will be enough for regression testing
        assert seasonValues == [0.9302895649920525, 0.9980629019785198, 1.1551483413078523, 0.9164991917215755], "Season Values are not initialized correctly"    # pragma: no cover

    def preset_season_factor_test(self):
        """Initial Season Factors should be presetable"""
        hwm = HoltWintersMethod(seasonLength=4)
        factors = [0,1,2,3]
        hwm.set_parameter("seasonValues", factors)

        data = [[0, 362.0], [1,385.0], [2, 432.0], [3, 341.0], [4, 382.0], [5, 409.0], [6, 498.0], [7, 387.0], [8, 473.0], [9, 513.0], [10, 582.0], [11, 474.0]]
        tsSrc = TimeSeries.from_twodim_list(data)
        seasonValues = hwm.initSeasonFactors(tsSrc)

        assert seasonValues == factors, "Preset Season Factors are not returned by initSeasonFactors"

        hwm.set_parameter("seasonValues", factors[:2])
        try:
            hwm.initSeasonFactors(tsSrc)
        except AssertionError:
            pass
        else:
            assert False, "If preset season factors and season length do not comply, initSeasonFactors should throw an AssertionError"    # pragma: no cover

    def initial_trend_values_test(self):
        hwm = HoltWintersMethod(seasonLength=4)
        data = [[0, 362.0], [1,385.0], [2, 432.0], [3, 341.0], [4, 382.0], [5, 425.0]]
        tsSrc = TimeSeries.from_twodim_list(data)
        trend = hwm.initialTrendSmoothingFactors(tsSrc)

        assert trend == 7.5, "Initial Trend should be 7.5 but is %f" % trend

    def season_length_test(self):
        """Test that the season length has to be greater than 0."""
        for seasonLength in xrange(-4, 1):
            try:
                HoltWintersMethod(seasonLength=seasonLength)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

        for seasonLength in xrange(1,12414, 412):
            HoltWintersMethod(seasonLength=seasonLength)
