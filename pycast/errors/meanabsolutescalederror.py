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

from pycast.errors import BaseErrorMeasure

class MeanAbsoluteScaledError(BaseErrorMeasure):
    """Implements the mean absolute scaled error.

    R J Hyndman and A B Koehler, "Another look at measures of forecast accuracy"
    """
    
    def __init__(self, minimalErrorCalculationPercentage=60, historyLength=10.0):
        """Initializes the error measure.

        :param Integer minimalErrorCalculationPercentage:    The number of entries in an
            original TimeSeries that have to have corresponding partners in the calculated
            TimeSeries. Corresponding partners have the same time stamp.
            Valid values are in [0.0, 100.0].
        :param Numeric historyLength:    Length of the TimeSeries used to calculate the mean
            of the history. If this is an Integer, the last historyLength data points will be used.
            If this is a Float, the last historyLength percent of the TimeSeries will be used for
            error calculation.

        :raise: Raises a :py:exc:`ValueError` if minimalErrorCalculationPercentage is not
            in [0.0, 100.0].
        :raise: Raises a :py:exc:`ValueError` if historyLength is a Float and not 
            in (0.0, 100.0).
        :raise: Raises a :py:exc:`ValueError` if historyLength + minimalErrorCalculationPercentage
            is not in (0.0, 100.0].
        """
        if not 0.0 < historyLength < 100.0:
            raise ValueError("historyLength has to be in (0.0, 100.0).")
        
        if isinstance(historyLength, float) and (historyLength + minimalErrorCalculationPercentage) > 100.0:
            raise ValueError("historyLength + minimalErrorCalculationPercentage has to be in (0.0, 100.0].")

        super(MeanAbsoluteScaledError, self).__init__(minimalErrorCalculationPercentage)
        self._historyLength = historyLength

    def _calculate(self, startingPercentage, endPercentage):
        """This is the error calculation function that gets called by :py:meth:`BaseErrorMeasure.get_error`.

        Both parameters will be correct at this time.

        :param Float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started.
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param Float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the vlaue, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.

        :return:    Returns a float representing the error.
        :rtype:     Float

        :raise:    Raises a :py:exc:`NotImplementedError` if the child class does not overwrite this method.
        """
        ## get the defined subset of error values
        errorValues = self._get_error_values(startingPercentage, endPercentage)

        ## Implement the error calculation here!

    def local_error(self, originalValue, calculatedValue):
        """Calculates the error between the two given values.

        :param Numeric originalValue:    Value of the original data.
        :param Numeric calculatedValue:    Value of the calculated TimeSeries that
            corresponds to originalValue.

        :return:    Returns the error measure of the two given values.
        :rtype:     Numeric

        :raise:    Raises a :py:exc:`NotImplementedError` if the child class does not overwrite this method.
        """
        ## Implement the local error calculation here!

MASE = MeanAbsoluteScaledError
