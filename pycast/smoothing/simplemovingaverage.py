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

from smoothingmethod import SmoothingMethod
from pycast.common.timeseries import TimeSeries

class SimpleMovingAverage(SmoothingMethod):
    """Implements the simple moving average.

    The SMA algorithm will calculate the average value at time t based on the
    datapoints between [t - floor(windowsize / 2), t + floor(windowsize / 2)].

    Explanation: http://en.wikipedia.org/wiki/Moving_average
    """

    def __init__(self, windowsize=5):
        """Initializes the SimpleMovingAverage.

        @param windowsize Size of the SimpleMovingAverages window.
                          This number has to be uneven and positive.
        """
        super(SimpleMovingAverage, self).__init__(["windowsize"], True, True)
        self.add_parameter("windowsize", windowsize)

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the SMA values for the predefined windowsize.

        @return TimeSeries object containing the smooth moving average.
        
        @todo This implementation aims to support independent for loop execution.
        """
        res = TimeSeries()

        minIdx = len(timeSeries) / 2

        windowsize = self._parameters["windowsize"]
        tsLength = len(timeSeries)
        for idx in xrange(tsLength - windowsize + 1):
            end = idx + windowsize
            data = timeSeries[idx:end]

            timestamp = data[windowsize//2][0]
            value     = sum([i[1] for i in data])/windowsize

            res.add_entry(timestamp, value)

        res.sort_timeseries()
        return res
