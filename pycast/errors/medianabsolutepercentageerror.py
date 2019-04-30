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

from pycast.errors.meanabsolutepercentageerror import MeanAbsolutePercentageError


class MedianAbsolutePercentageError(MeanAbsolutePercentageError):

    """Represents the median absolute percentage error."""

    def _calculate(self, starting_percentage: float, end_percentage: float, start_date, end_date):
        """This is the error calculation function that gets called by :py:meth:`BaseErrorMeasure.get_error`.

        Both parameters will be correct at this time.

        Args:
        float starting_percentage (float): Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started.
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        end_percentage (float):    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.
        start_date (float): Epoch representing the start date used for error calculation.
        float end_date (float): Epoch representing the end date used in the error calculation.

        Returns:
            float: Returns a float representing the error value.
        """
        # get the defined subset of error values
        error_values = self._get_error_values(starting_percentage, end_percentage, start_date, end_date)
        error_values = list(filter(lambda e: e is not None, error_values))

        return sorted(error_values)[len(error_values)//2]


MdAPE = MedianAbsolutePercentageError
