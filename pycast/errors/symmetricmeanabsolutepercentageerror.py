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

from pycast.errors.baseerrormeasure import BaseErrorMeasure

class SymmetricMeanAbsolutePercentageError(BaseErrorMeasure):

    """Implements the symmetric mean absolute percentage error whose values are
    between 0 and 200%.

    Explanation:
    http://www.stat.iastate.edu/preprint/articles/2004-10.pdf (page 14)

    If the calculated value and the original value are equal, the error is 0.
    """

    def _calculate(self, startingPercentage, endPercentage, startDate, endDate):
        """This is the error calculation function that gets called by :py:meth:`BaseErrorMeasure.get_error`.

        Both parameters will be correct at this time.

        :param float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started.
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.
        :param float startDate: Epoch representing the start date used for error calculation.
        :param float endDate: Epoch representing the end date used in the error calculation.

        :return:    Returns a float representing the error.
        :rtype: float
        """
        # get the defined subset of error values
        errorValues = self._get_error_values(startingPercentage, endPercentage, startDate, endDate)

        return float(sum(errorValues)) / float(len(errorValues))

    def local_error(self, originalValue, calculatedValue):
        """Calculates the error between the two given values.

        :param list originalValue:    List containing the values of the original data.
        :param list calculatedValue:    List containing the values of the calculated TimeSeries that
            corresponds to originalValue.

        :return:    Returns the error measure of the two given values.
        :rtype:     numeric
        """
        originalValue = originalValue[0]
        calculatedValue = calculatedValue[0]

        # error is zero
        if not originalValue and not calculatedValue:
            return 0.0

        return abs(calculatedValue - originalValue)/ ((abs(originalValue) + abs(calculatedValue))/2) * 100

#        originalValue = originalValue[0]
#
#
#        # error is zero
#        if originalValue == calculatedValue:
#            return 0.0
#
#        return (abs(calculatedValue - originalValue) / ((originalValue + calculatedValue) / 2))

SMAPE = SymmetricMeanAbsolutePercentageError
