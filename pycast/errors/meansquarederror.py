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

from baseerrormeasure import BaseErrorMeasure

class MeanSquaredError(BaseErrorMeasure):
    """Implements the mean squared error measure.

    Explanation:
        http://en.wikipedia.org/wiki/Mean_squared_error
    """

    def calculate(self, originalTimeSeries, calculatedTimeSeries):
        """Calculates the error for the given calculated TimeSeries.

        To calculate the error between the given TimeSeries instances, only entries with
        matching timestamps are considered. To optimize the calculation, both TimeSeries
        instances will be sorted inplace.

        @param originalTimeSeries   TimeSeries containing the original data.
        @param calculatedTimeSeries TimeSeries containing calculated data.
                                    Calculated data is smoothed or forecasted data.

        @return Returns True if an error could be calculated, False otherwise.
        """
        ## sort the TimeSeries to reduce the required comparison operations
        originalTimeSeries.sort_timeseries()
        calculatedTimeSeries.sort_timeseries()

        ## Performance optimization
        append      = self._errorValues.append
        minCalcIdx  = 0
        local_error = self.local_error

        ## calculate all valid local errors
        for orgPair in originalTimeSeries:
            for calcIdx in xrange(minCalcIdx, len(calculatedTimeSeries)):
                calcPair = calculatedTimeSeries[calcIdx]

                ## Skip values that can not be compared
                if calcPair[0] < orgPair[0]:
                    continue
                if calcPair[0] > orgPair[0]:
                    break

                append(local_error(orgPair[1], calcPair[1]))

        ## return False, if the error cannot be calculated
        if len(self._errorValues) < self._minimalErrorCalculationPercentage * len(originalTimeSeries):
            self._errorValues = []
            return False

        ## calculate the resulting error
        self._error = float(sum(self._errorValues) / float(len(self._errorValues)))

        return True

    def local_error(self, originalValue, calculatedValue):
        """Calculates the error between the two given values.

        @param originalValue   Value of the original data.
        @param calculatedValue Value of the calculated TimeSeries that
                               corresponds to originalValue.

        @return Returns the squared error:
                (calculatedValue - originalValue)^2
        """
        return (calculatedValue - originalValue)**2