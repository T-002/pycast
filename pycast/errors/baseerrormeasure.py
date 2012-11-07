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

class BaseErrorMeasure(object):
    """Baseclass for all error measures."""

    def __init__(self, minimalErrorCalculationPercentage=60):
        """Initializes the error measure.

        @param minimalErrorCalculationPercentage The number of entries in an
                   original TimeSeries that have to have corresponding partners
                   in the calculated TimeSeries. Corresponding partners have
                   the same time stamp.
                   Valid values are [0.0, 100.0].

        @throw ValueError Throws a ValueError, if minimalErrorCalculationPercentage is not
                          in [0.0, 100.0].
        """
        super(BaseErrorMeasure, self).__init__()

        if not 0.0 <= minimalErrorCalculationPercentage <= 100.0:
            raise ValueError("minimalErrorCalculationPercentage has to be in [0.0, 100.0].")

        self._minimalErrorCalculationPercentage = minimalErrorCalculationPercentage / 100.0

        self._error = None
        self._errorValues = []

    def __lt__(self, otherErrorMeasure):
        """Returns if the error is smaller than the error of otherErrorMeasure.

        @return Returns True, if the error is smaller, False otherwise.

        @throw Throws a ValueError, of self and otherErrorMeasure are not an instance
               of the same error measure.
        """
        if not self.__class__ == otherErrorMeasure.__class__:
            raise ValueError("Only error measures of the same class can be compared.")

        return self._error < otherErrorMeasure.get_error()
    
    def get_error(self):
        """Returns the overall error.

        @return Returns a float representing the error value of the error measure.
                Returns None if the error was not calculate(d) yet.
        """
        return self._error

    def calculate(self, originalTimeSeries, calculatedTimeSeries):
        """Calculates the error for the given calculated TimeSeries.

        To calculate the error between the given TimeSeries instances, only entries with matching
        timestamps are considered.

        @param originalTimeSeries   TimeSeries containing the original data.
        @param calculatedTimeSeries TimeSeries containing calculated data.
                                    Calculated data is smoothed or forecasted data.

        @return Return True if the error could be calculated, False otherwise.
        """
        raise NotImplementedError

    def local_error(self, originalValue, calculatedValue):
        """Calculates the error between the two given values.

        @param originalValue   Value of the original data.
        @param calculatedValue Value of the calculated TimeSeries that
                               corresponds to originalValue.

        @return Returns the error measure of the two given values.
        """
        raise NotImplementedError
