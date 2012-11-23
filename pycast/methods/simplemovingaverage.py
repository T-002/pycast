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

from pycast.methods import BaseMethod
from pycast.common.timeseries import TimeSeries

class SimpleMovingAverage(BaseMethod):
    """Implements the simple moving average.

    The SMA algorithm will calculate the average value at time t based on the
    datapoints between [t - floor(windowsize / 2), t + floor(windowsize / 2)].

    Explanation:
        http://en.wikipedia.org/wiki/Moving_average
    """

    def __init__(self, windowsize=5):
        """Initializes the SimpleMovingAverage.

        :param Integer windowsize:    Size of the SimpleMovingAverages window.
        
        :raise:    Raises a :py:exc:`ValueError` if windowsize is an even or not larger than zero.
        """
        if windowsize <= 0:
            raise ValueError("windowsize has to be larger than 0.")
        if windowsize/2 == windowsize/2.0:
            raise ValueError("windowsize has to be uneven.")

        super(SimpleMovingAverage, self).__init__(["windowsize"], True, True)
        self.set_parameter("windowsize", windowsize)

    def _get_parameter_intervals(self):
        """Returns the intervals for the methods parameter.

        Only parameters with defined intervals can be used for optimization!

        :return:    Returns a dictionary containing the parameter intervals, using the parameter
            name as key, while the value hast the following format:
            [minValue, maxValue, minIntervalClosed, maxIntervalClosed]

                - minValue
                    Minimal value for the parameter
                - maxValue
                    Maximal value for the parameter
                - minIntervalClosed
                    :py:const:`True`, if minValue represents a valid value for the parameter.
                    :py:const:`False` otherwise.
                - maxIntervalClosed:
                    :py:const:`True`, if maxValue represents a valid value for the parameter.
                    :py:const:`False` otherwise.
        :rtype:     Dictionary
        """
        parameterIntervals = {}

        return parameterIntervals

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the SMA values for the predefined windowsize.

        :param TimeSeries timeSeries:    The TimeSeries used to calculate the simple moving average values.

        :return:    TimeSeries object containing the smooth moving average.
        :rtype:     TimeSeries
        
        :raise:   Raises a :py:exc:`ValueError` wif the defined windowsize is larger than the number of elements
            in timeSeries

        :note:    This implementation aims to support independent for loop execution.
        """
        windowsize    = self._parameters["windowsize"]

        if len (timeSeries) < windowsize:
            raise ValueError("windowsize is larger than the number of elements in timeSeries.")

        minIdx = len(timeSeries) / 2
        
        tsLength      = len(timeSeries)
        nbrOfLoopRuns = tsLength - windowsize + 1

        res = TimeSeries()        
        for idx in xrange(nbrOfLoopRuns):
            end = idx + windowsize
            data = timeSeries[idx:end]

            timestamp = data[windowsize//2][0]
            value     = sum([i[1] for i in data])/windowsize

            res.add_entry(timestamp, value)

        res.sort_timeseries()
        return res
