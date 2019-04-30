# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# Copyright (c) 2012-2019 Christian Schwarz
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
import pytest

# required modules from pycast
from pycast.common.timeseries import TimeSeries
from pycast.common.pycastobject import PyCastObject
from pycast.errors.baseerrormeasure import BaseErrorMeasure
from pycast.errors.meansquarederror import MeanSquaredError


class TestBaseErrorMeasure:
    """Test cases for the BaseErrorMeasure class."""

    def test_initialization_without_parameters(self):
        """Tests the initialization without configured parameters."""
        BaseErrorMeasure()

    @pytest.mark.parametrize("percentage", [0.0, 12.23, 42.12, 100.0])
    def test_correct_initialization(self, percentage):
        """Tests the initialization with correct values.

        Args:
            percentage (numeric): Value to be tested during the initialization process.
        """
        BaseErrorMeasure(percentage)

    @pytest.mark.parametrize("percentage", [-1.2, -0.1, 100.1, 123.42])
    def test_initialization_with_invalid_parameters(self, percentage):
        """Tests the initialization with invalid parameters.

        Args:
            percentage (numeric): Value to be tested during the initialization process.
        """
        with pytest.raises(Exception):
            BaseErrorMeasure(percentage)

    def test_get_error_initialization(self):
        """Test the get_error of BaseErrorMeasure for the expected exception."""
        bem = BaseErrorMeasure()

        with pytest.raises(Exception):
            bem.get_error()

    # todo: Add a mock here for _calculate and local_error
    def test_double_initialization(self):
        """Test for the error occurring when the same error measure is initialized twice."""
        data = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        original_timeseries = TimeSeries.from_twodim_list(data)
        calculated_timeseries = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        bem_calculate = bem._calculate
        bem_local_error = bem.local_error

        def return_zero(*args):
            return 0

        # remove the NotImplementedErrors for initialization
        bem.local_error = return_zero
        bem._calculate = return_zero

        # correct initialize call
        bem.initialize(original_timeseries, calculated_timeseries)

        # duplicated call that should raise the exception
        with pytest.raises(Exception):
            bem.initialize(original_timeseries, calculated_timeseries)

        bem.local_error = bem_calculate
        bem._calculate = bem_local_error

    def test_initialization(self):
        """Test if calculate throws an error as expected."""
        data = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        original_timeseries = TimeSeries.from_twodim_list(data)
        calculated_timeseries = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        try:
            bem.initialize(original_timeseries, calculated_timeseries)
        except NotImplementedError:
            pass
        else:
            assert False, "A NotImplementedError should have occurred."

        assert not bem.initialize(original_timeseries, TimeSeries())

    # todo: Add mock here
    @pytest.mark.xfail(raises=ValueError)
    def test_get_error_parameter(self):
        """Test for the parameter validity of get_error()."""
        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        original_timeseries = TimeSeries.from_twodim_list(data)
        calculated_timeseries = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        bem_calculate = bem._calculate
        bem_local_error = bem.local_error

        def return_zero(*args):
            return 0

        # remove the NotImplementedErrors for initialization
        bem.local_error = return_zero
        bem._calculate = return_zero
        bem.initialize(original_timeseries, calculated_timeseries)

        bem.local_error = bem_local_error
        bem._calculate = bem_calculate

        try:
            bem.get_error(10.0, 90.0)
        except NotImplementedError:
            pass
        else:
            assert False, "A NotImplementedError should have occurred."

        for start in [-1.0, 80.0, 103.0]:
            for end in [-5.0, 10.0, 105.0]:
                 bem.get_error(start, end)

    def test_local_error(self):
        """Test local_error of BaseErrorMeasure."""
        data = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        original_timeseries  = TimeSeries.from_twodim_list(data)
        calculated_timeseries = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        for idx in range(len(original_timeseries)):
            with pytest.raises(NotImplementedError):
                bem.local_error([original_timeseries[idx][1]], [calculated_timeseries[idx][1]])

    def test_optimized(self):
        """Check if all tests are passed, using optimized implementations."""
        PyCastObject.enable_global_optimization()
        self.test_get_error_initialization()
        self.test_initialization()
        self.test_double_initialization()
        PyCastObject.disable_global_optimization()

    def test_confidence_intervals(self,):
        """Tests the retrieval of confidence interval values."""
        bem = BaseErrorMeasure()
        bem._errorValues = [10, -5, 3, -4, None, 0, 2, -3]

        assert bem.confidence_interval(0.5) == (-3.0, 2.0)
        assert bem.confidence_interval(0.1) == (0.0, 0.0)

    @pytest.mark.parametrize("interval", [-0.5, 2.42])
    def test_confidence_intervals_with_invalid_borders(self, interval):
        """Tests the retrieval of confidence interval values with invalid borders.

        Args:
            interval (float): Interval value to be tested.
        """
        bem = BaseErrorMeasure()
        bem._errorValues = [10, -5, 3, -4, None, 0, 2, -3]

        with pytest.raises(ValueError):
            bem.confidence_interval(interval)

    def test_get_error_values(self):
        """Test the retrieval of error values."""
        bem = BaseErrorMeasure()
        bem._errorValues = [1, -1, 3, -5, 8]
        bem._errorDates = [1, 2, 3, 4, 5]

        assert bem._get_error_values(0,100, None, None) == [1,-1,3,-5,8]
        assert bem._get_error_values(0,100, 2, None) == [-1,3,-5,8]
        assert bem._get_error_values(0,100, None, 4) == [1,-1,3,-5]
        assert bem._get_error_values(0,100, 2, 4) == [-1,3,-5]

    def test_get_error_values_with_invalid_borders(self):
        """Tests the retrieval of error values with invalid borders."""
        bem = BaseErrorMeasure()
        bem._errorValues = [1, -1, 3, -5, 8]
        bem._errorDates = [1, 2, 3, 4, 5]

        with pytest.raises(ValueError):
            bem._get_error_values(0, 100, None, 0)

    def test_number_of_comparisons(self):
        """Test BaseErrorMeasure.initialize for behaviour if enough dates match."""
        data = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

        timeseries = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure(60.0)
        mse = MeanSquaredError(80.0)

        # prevent NotImplementedError
        bem.local_error = lambda a, b: 1

        assert mse.initialize(timeseries, timeseries)

    def test_number_of_comparisons_with_missing_data(self):
        """Test BaseErrorMeasure.initialize for behaviour if not enough dates match."""
        actual_data = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]
        calculated_data = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5.1, 5], [6.1, 6], [7.1, 7], [8.1, 8], [9.1, 9]]

        actual_timeseries  = TimeSeries.from_twodim_list(actual_data)
        calculated_timeseries = TimeSeries.from_twodim_list(calculated_data)

        bem = BaseErrorMeasure(60.0)
        mse = MeanSquaredError(80.0)

        # prevent NotImplementedError
        bem.local_error = lambda a, b: 1

        # only 50% of the original TimeSeries have a corresponding partner
        assert not mse.initialize(actual_timeseries, calculated_timeseries)

    def test_valid_error_calculation(self):
        """Test for a valid error calculation."""
        original_data = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8],   [9, 9]]
        calculated_data = [[0, 1], [1, 3], [2, 5], [3, 0], [4, 3], [5, 5], [6.1, 6], [7, 3], [8.1, 8], [9, 8]]

        original_timeseries = TimeSeries.from_twodim_list(original_data)
        calculated_timeseries = TimeSeries.from_twodim_list(calculated_data)

        error_measure = MeanSquaredError(80.0)
        error_measure.initialize(original_timeseries, calculated_timeseries)

        assert error_measure.get_error() == 5.125
