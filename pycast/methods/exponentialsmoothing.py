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
                               Valid values are [0.0, 1.0].
        @param valuesToForecast Defines the number of forecasted values that will
               be part of the result.

        @raises ValueError, when smoothingFactor has an invalid value.
        """
        super(ExponentialSmoothing, self).__init__(["smoothingFactor", "valuesToForecast"], True, True)

        if not 0.0 <= smoothingFactor <= 1.0:
            raise ValueError("smoothingFactor has to be in [0.0, 1.0].")
        
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

            for idx in xrange(valuesToForecast):
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
        """Initializes the HoltMethod.

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
        for idx in xrange(len(timeSeries)):
            ## initialization for s_1 and b_1
            if 0 == idx:
               sOld = timeSeries[idx][1]
               b = timeSeries[idx+1][1]-timeSeries[idx][1]
               continue

            sNew = (alpha * timeSeries[idx-1][1]) + ((1 - alpha) * (sOld + b))
            b    = (beta * (sNew - sOld)) + ((1 - beta) * b)
            sOld = sNew

            res.add_entry(timeSeries[idx][0], sOld)

        ## forecast additional values if requested
        if valuesToForecast > 0:
            startTime          = res[-1][0]
            normalizedTimeDiff = startTime - res[-2][0]

            for idx in xrange(valuesToForecast):
                startTime += normalizedTimeDiff

                s = sOld + idx * b
                res.add_entry(startTime, s)

        ## return the resulting TimeSeries :)
        return res
    
    ## TODO:A second method, referred to as either Brown's linear exponential smoothing (LES) or Brown's double exponential smoothing works as follows.[9]

class HoltWintersMethod(BaseMethod):
    """Implements the Holt-Winters algorithm.

    Explanation: http://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing

    @todo NotImplementedYet
    """

    def __init__(self, smoothingFactor=0.1, trendSmoothingFactor=0.5, seasonLength=42, valuesToForecast=1):
        """Initializes the HoltWintersMethod.

        @param smoothingFactor Defines the alpha for the HoltMethod.
        @param trendSmoothingFactor Defines the beta for the HoltMethod.
        @param seasonLength The expected length for the seasons. Please use a good estimate here!
        @param valuesToForecast Defines the number of forecasted values that will
               be part of the result.
        """
        super(HoltWintersMethod, self).__init__(["smoothingFactor",
                                          "trendSmoothingFactor", 
                                          "valuesToForecast",
                                          "seasonLength"],
                                          True, True)

        self.add_parameter("smoothingFactor",      smoothingFactor)
        self.add_parameter("trendSmoothingFactor", trendSmoothingFactor)
        seld.add_parameter("seasonLength",         seasonLength)
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

        ## @todo THIS IS NOT IMPLEMENTED YET

        ## return the resulting TimeSeries :)
        return re