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

    Explanation:
        http://www.youtube.com/watch?v=J4iODLa9hYw
    """

    def __init__(self, smoothingFactor=0.1, valuesToForecast=1):
        """Initializes the ExponentialSmoothing.

        @param smoothingFactor Defines the alpha for the ExponentialSmoothing.
                               Valid values are (0.0, 1.0).
        œparam valuesToForecast Number of values that should be forecasted.

        @throw ValueError, when smoothingFactor has an invalid value.
        """
        super(ExponentialSmoothing, self).__init__(["smoothingFactor", "valuesToForecast"], True, True)

        if not 0.0 < smoothingFactor < 1.0:
            raise ValueError("smoothingFactor has to be in (0.0, 1.0).")

        self.add_parameter("smoothingFactor",  smoothingFactor)
        self.add_parameter("valuesToForecast", valuesToForecast)


    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values and one forecasted one.

        @return TimeSeries object containing the exponentially smoothed TimeSeries,
                including the forecasted value.
        
        @todo Currently the first normalized value is simply chosen as the starting point.
        """
        ## extract the required parameters, performance improvement
        alpha            = self._parameters["smoothingFactor"]
        valuesToForecast = self._parameters["valuesToForecast"]

        ## initialize some variables
        resultList  = []
        estimator   = None
        lastT       = None
        
        ## "It's always about performance!"
        append = resultList.append

        ## smooth the existing TimeSeries data
        for idx in xrange(len(timeSeries)):
            ## get the current to increase performance
            t = timeSeries[idx]

            ## get the initial estimate
            if None == estimator:
                estimator = t[1]
                continue

            ## add the first value to the resultList without any correction
            if 0 == len(resultList):
                append([t[0], estimator])
                lastT = t
                continue

            ## calculate the error made during the last estimation
            error = lastT[1] - estimator

            ## calculate the new estimator, based on the last occured value, the error and the smoothingFactor
            estimator = estimator + alpha * error

            ## save the current value for the next iteration
            lastT = t

            ## add an entry to the result
            append([t[0], estimator])

        ## forecast additional values if requested
        if valuesToForecast > 0:
            currentTime        = resultList[-1][0]
            normalizedTimeDiff = currentTime - resultList[-2][0]

            for idx in xrange(valuesToForecast):
                currentTime += normalizedTimeDiff

                ## reuse everything
                error     = lastT[1] - estimator
                estimator = estimator + alpha * error

                ## add a forecasted value
                append([currentTime, estimator])

                ## set variables for next iteration
                lastT         = resultList[-1]
        
        ## return a TimeSeries, containing the result
        return TimeSeries.from_twodim_list(resultList)

class HoltMethod(BaseMethod):
    """Implements the Holt algorithm.

    Explanation:
        http://en.wikipedia.org/wiki/Exponential_smoothing#Double_exponential_smoothing
    """

    def __init__(self, smoothingFactor=0.1, trendSmoothingFactor=0.5, valuesToForecast=1):
        """Initializes the HoltMethod.

        @param smoothingFactor Defines the alpha for the HoltMethod.
                               Valid values are (0.0, 1.0).
        @param trendSmoothingFactor Defines the beta for the HoltMethod.
                                    Valid values are (0.0, 1.0).
        @param valuesToForecast Defines the number of forecasted values that will
               be part of the result.

        @raises ValueError, when smoothingFactor or trendSmoothingFactor has an invalid value.
        """
        super(HoltMethod, self).__init__(["smoothingFactor",
                                          "trendSmoothingFactor", 
                                          "valuesToForecast"],
                                          True, True)

        if not 0.0 < smoothingFactor < 1.0:
            raise ValueError("smoothingFactor has to be in (0.0, 1.0).")
        if not 0.0 < trendSmoothingFactor < 1.0:
            raise ValueError("trendSmoothingFactor has to be in (0.0, 1.0).")

        self.add_parameter("smoothingFactor",      smoothingFactor)
        self.add_parameter("trendSmoothingFactor", trendSmoothingFactor)
        self.add_parameter("valuesToForecast",     valuesToForecast)

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values.

        @return TimeSeries object containing the exponentially smoothed TimeSeries,
                including the forecasted values.
        
        @todo Currently the first normalized value is simply chosen as the starting point.
        """
        ## extract the required parameters, performance improvement
        alpha            = self._parameters["smoothingFactor"]
        beta             = self._parameters["trendSmoothingFactor"]
        valuesToForecast = self._parameters["valuesToForecast"]

        ## initialize some variables
        resultList  = []
        estimator   = None
        trend       = None
        lastT       = None

        ## "It's always about performance!"
        append = resultList.append

        ## smooth the existing TimeSeries data
        for idx in xrange(len(timeSeries)):
            ## get the current to increase performance
            t = timeSeries[idx]

            ## get the initial estimate
            if None == estimator:
                estimator = t[1]
                lastT     = t
                continue

            ## add the first value to the resultList without any correction
            if 0 == len(resultList):
                append([t[0], estimator])
                trend         = t[1] - lastT[1]
                
                ## store current values for next iteration
                lastT         = t
                lastEstimator = estimator
                continue

            ## calculate the new estimator and trend, based on the last occured value, the error and the smoothingFactor
            estimator = alpha * t[1] + (1 - alpha) * (estimator + trend)
            trend     = beta * (estimator - lastEstimator) + (1 - beta) * trend

            ## add an entry to the result
            append([t[0], estimator])

            ## store current values for next iteration
            lastT         = t
            lastEstimator = estimator

        ## forecast additional values if requested
        if valuesToForecast > 0:
            currentTime        = resultList[-1][0]
            normalizedTimeDiff = currentTime - resultList[-2][0]

            for idx in xrange(1, valuesToForecast + 1):
                currentTime += normalizedTimeDiff

                ## reuse everything
                forecast = estimator + idx * trend

                ## add a forecasted value
                append([currentTime, forecast])

        ## return a TimeSeries, containing the result
        return TimeSeries.from_twodim_list(resultList)
    
## TODO:A second method, referred to as either Brown's linear exponential smoothing (LES) or Brown's double exponential smoothing works as follows.[9]

class HoltWintersMethod(BaseMethod):
    """Implements the Holt-Winters algorithm.

    Explanation:
        http://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing

    @todo NotImplementedYet
    """

    def __init__(self, smoothingFactor=0.1, trendSmoothingFactor=0.5, seasonSmoothingFactor=0.5, seasonLength=42, valuesToForecast=1):
        """Initializes the HoltWintersMethod.

        @param smoothingFactor Defines the alpha for the Holt-Winters algorithm.
                               Valid values are (0.0, 1.0).
        @param trendSmoothingFactor Defines the beta for the Holt-Winters algorithm..
                                    Valid values are (0.0, 1.0).
        @param seasonSmoothingFactor Defines the gamma for the Holt-Winters algorithm.
                                     Valid values are (0.0, 1.0). 
        @param seasonLength The expected length for the seasons. Please use a good estimate here!
        @param valuesToForecast Defines the number of forecasted values that will
               be part of the result.
        """
        super(HoltWintersMethod, self).__init__(["smoothingFactor",
                                          "trendSmoothingFactor",
                                          "seasonSmoothingFactor"
                                          "valuesToForecast",
                                          "seasonLength"],
                                          True, True)

        if not 0.0 < smoothingFactor < 1.0:
            raise ValueError("smoothingFactor has to be in (0.0, 1.0).")
        if not 0.0 < trendSmoothingFactor < 1.0:
            raise ValueError("trendSmoothingFactor has to be in (0.0, 1.0).")
        if not 0.0 < seasonSmoothingFactor < 1.0:
            raise ValueError("seasonSmoothingFactor has to be in (0.0, 1.0).")

        self.add_parameter("smoothingFactor",      smoothingFactor)
        self.add_parameter("trendSmoothingFactor", trendSmoothingFactor)
        self.add_parameter("seasonSmoothingFactor", seasonSmoothingFactor)
        self.add_parameter("seasonLength",         seasonLength)
        self.add_parameter("valuesToForecast",     valuesToForecast)

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values.

        @return TimeSeries object containing the exponentially smoothed TimeSeries,
                including the forecasted values.
        
        @todo Double check if it is correct not to add the first original value to the result.
        @todo Currently the first normalized value is simply chosen as the starting point.
        """
        raise NotImplementedError    # pragma: no cover