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

    def __init__(self):
        """Initializes the error measure."""
        super(BaseErrorMeasure, self).__init__()

        self._error = None

    def get_error(self):
        """Returns the overall error.

        @return Returns a float representing the error value of the error measure.
                Returns None if the error was not calculate(d) yet.
        """
        return self._error

    def calculate(self, originalTimeSeries, calculatedTimeSeries):
        """Calculates the error for the given calculated TimeSeries.

        @param originalTimeSeries   TimeSeries containing the original data.
        @param calculatedTimeSeries TimeSeries containing calculated data.
                                    Calculated data is smoothed or forecasted data.
        """
        raise NotImplementedError