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

from pycast.errors.baseerrormeasure import BaseErrorMeasure


class MeanSquaredError(BaseErrorMeasure):
    """Implements the mean squared error measure.

    Explanation:
        http://en.wikipedia.org/wiki/Mean_squared_error
    """

    def _calculate(self, starting_percentage: float, end_percentage: float, start_date: float, end_date: float):
        """This is the error calculation function that gets called by BaseErrorMeasure.get_error.

        Args:
            starting_percentage (float): Defines the start of the interval. This has to be a value in [0.0, 100.0].
                It represents the value, where the error calculation should be started.
                25.0 for example means that the first 25% of all calculated errors will be ignored.

            end_percentage (float): Defines the end of the interval. This has to be a value in [0.0, 100.0].
                It represents the value, after which all error values will be ignored. 90.0 for example means that
                the last 10% of all local errors will be ignored.
            start_date (float): Epoch representing the start date used for error calculation.
            end_date (float): Epoch representing the end date used in the error calculation.

        Returns:
            float: Returns a float representing the error.
        """
        # get the defined subset of error values
        error_values = self._get_error_values(starting_percentage, end_percentage, start_date, end_date)
        return sum(error_values) / len(error_values)

    def local_error(self, original_values: list, calculated_values: list):
        """Calculates the error between the two given values.

        Args:
            original_value (list): List containing the values of the original data.
            calculated_value (list): List containing the values of the calculated TimeSeries that
                corresponds to original_values.

        Returns:
            float: Calculated error value.
        """
        error_value = 0
        for idx in range(len(original_values)):
            error_value += (calculated_values[idx] - original_values[idx])**2

        return error_value


MSE = MeanSquaredError
