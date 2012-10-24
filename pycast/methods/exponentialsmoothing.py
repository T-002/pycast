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

from basemethod import BaseMethod
from pycast.common.timeseries import TimeSeries

class ExponentialSmoothing(BaseMethod):
    """Implements an exponential smoothing algorithm.

    Explanation: http://en.wikipedia.org/wiki/Exponential_smoothing
    """

    def __init__(self, smoothingFactor=0.1, valuesToForecast=1):
        """Initializes the ExponentialSmoothing.

        @param smoothingFactor Defines the alpha for the ExponentialSmoothing.
        @param valuesToForecast Defines the number of forecasted values that will
               be part of the result.
        """
        super(ExponentialSmoothing, self).__init__(["smoothingFactor", "valuesToForecast"], True, True)
        self.add_parameter("smoothingFactor", smoothingFactor)
        self.add_parameter("valuesToForecast", valuesToForecast)

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values.

        @return TimeSeries object containing the exponentially smoothed TimeSeries,
                including the forecasted values.
        
        @todo Double check if it is correct not to add the first original value to the result.
        @todo Currently the first normalized value is simply chosen as the starting point.
        """
        ## initialize the result TimeSeries
        res = TimeSeries()

        ## extract the required parameters, performance improvement
        alpha            = self._parameters["smoothingFactor"]
        valuesToForecast = self._parameters["valuesToForecast"]

        ## smooth the existing TimeSeries data
        for idx in xrange(len(timeSeries)):
            if 0 == idx:
                s = timeSeries[idx][1]
                continue

            s = (alpha * timeSeries[idx-1][1]) + ((1 - alpha) * s)

            res.add_entry(timeSeries[idx][0], s)

        ## forecast additional values if requested
        if valuesToForecast > 0:
            startTime          = res[-1][0]
            normalizedTimeDiff = startTime - res[-2][0]

            for idx in xrange(self._parameters["valuesToForecast"]):
                startTime += normalizedTimeDiff

                s = (alpha * res[-1][1]) + ((1 - alpha) * s)
                res.add_entry(startTime, s)

        ## return the resulting TimeSeries :)
        return res

class HoltMethod(BaseMethod):
    """Implements the Holt algorithm.

    Explanation: http://en.wikipedia.org/wiki/Exponential_smoothing#Double_exponential_smoothing
    """

    def __init__(self, smoothingFactor=0.1, trendSmoothingFactor=0.5, valuesToForecast=1):
        """Initializes the ExponentialSmoothing.

        @param smoothingFactor Defines the alpha for the HoltMethod.
        @param trendSmoothingFactor Defines the beta for the HoltMethod.
        @param valuesToForecast Defines the number of forecasted values that will
               be part of the result.
        """
        super(HoltMethod, self).__init__(["smoothingFactor",
                                          "trendSmoothingFactor", 
                                          "valuesToForecast"],
                                          True, True)

        self.add_parameter("smoothingFactor",      smoothingFactor)
        self.add_parameter("trendSmoothingFactor", trendSmoothingFactor)
        self.add_parameter("valuesToForecast",     valuesToForecast)

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values.

        @return TimeSeries object containing the exponentially smoothed TimeSeries,
                including the forecasted values.
        
        @todo Double check if it is correct not to add the first original value to the result.
        @todo Currently the first normalized value is simply chosen as the starting point.
        """
        ## initialize the result TimeSeries
        res = TimeSeries()

        ## extract the required parameters, performance improvement
        alpha            = self._parameters["smoothingFactor"]
        beta             = self._parameters["trendSmoothingFactor"]
        valuesToForecast = self._parameters["valuesToForecast"]

        ## smooth the existing TimeSeries data
#       for idx in xrange(len(timeSeries)):
#           if 0 == idx:
#               s = timeSeries[idx][1]
#               continue
#
#           s = (alpha * timeSeries[idx-1][1]) + ((1 - alpha) * s)
#
#           res.add_entry(timeSeries[idx][0], s)

        ## forecast additional values if requested
#        if valuesToForecast > 0:
#            startTime          = res[-1][0]
#            normalizedTimeDiff = startTime - res[-2][0]
#
#            for idx in xrange(self._parameters["valuesToForecast"]):
#                startTime += normalizedTimeDiff
#
#                s = (alpha * res[-1][1]) + ((1 - alpha) * s)
#                res.add_entry(startTime, s)

        ## return the resulting TimeSeries :)
        return res