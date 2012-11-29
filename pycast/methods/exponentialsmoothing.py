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

from pycast.methods import BaseForecastingMethod
from pycast.common.timeseries import TimeSeries

class ExponentialSmoothing(BaseForecastingMethod):
    """Implements an exponential smoothing algorithm.

    Explanation:
        http://www.youtube.com/watch?v=J4iODLa9hYw
    """

    def __init__(self, smoothingFactor=0.1, valuesToForecast=1):
        """Initializes the ExponentialSmoothing.

        :param Float smoothingFactor:    Defines the alpha for the ExponentialSmoothing.
            Valid values are in (0.0, 1.0).
        :param Integer valuesToForecast:    Number of values that should be forecasted.

        :raise: Raises a :py:exc:`ValueError` when smoothingFactor has an invalid value.
        """
        super(ExponentialSmoothing, self).__init__(["smoothingFactor"], valuesToForecast, True, True)

        self.set_parameter("smoothingFactor",  smoothingFactor)

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

        parameterIntervals["smoothingFactor"] = [0.0, 1.0, False, False]

        return parameterIntervals

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed and forcasted values.

        :return:    TimeSeries object containing the smoothed TimeSeries,
           including the forecasted values.
        :rtype:     TimeSeries
        
        :note:    The first normalized value is chosen as the starting point.
        """
        ## determine the number of values to forecast, if necessary
        self._calculate_values_to_forecast(timeSeries)

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

class HoltMethod(BaseForecastingMethod):
    """Implements the Holt algorithm.

    Explanation:
        http://en.wikipedia.org/wiki/Exponential_smoothing#Double_exponential_smoothing
    """

    def __init__(self, smoothingFactor=0.1, trendSmoothingFactor=0.5, valuesToForecast=1):
        """Initializes the HoltMethod.

        :param Float smoothingFactor:    Defines the alpha for the ExponentialSmoothing.
            Valid values are in (0.0, 1.0).
        :param Float trendSmoothingFactor:    Defines the beta for the HoltMethod.
            Valid values are in (0.0, 1.0).
        :param Integer valuesToForecast:    Defines the number of forecasted values that will
            be part of the result.

        :raise:    Raises a :py:exc:`ValueError` when smoothingFactor or trendSmoothingFactor has an invalid value.
        """
        super(HoltMethod, self).__init__(["smoothingFactor",
                                          "trendSmoothingFactor"],
                                          valuesToForecast, True, True)

        self.set_parameter("smoothingFactor",      smoothingFactor)
        self.set_parameter("trendSmoothingFactor", trendSmoothingFactor)

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

        parameterIntervals["smoothingFactor"]      = [0.0, 1.0, False, False]
        parameterIntervals["trendSmoothingFactor"] = [0.0, 1.0, False, False]

        return parameterIntervals

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values.

        :return:    TimeSeries object containing the smoothed TimeSeries,
            including the forecasted values.
        :rtype:     TimeSeries
        
        :note: The first normalized value is chosen as the starting point.
        """
        ## determine the number of values to forecast, if necessary
        self._calculate_values_to_forecast(timeSeries)

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

class HoltWintersMethod(BaseForecastingMethod):
    """Implements the Holt-Winters algorithm.

    Explanation:
        http://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing
    """

    def __init__(self, smoothingFactor=0.1, trendSmoothingFactor=0.5, seasonSmoothingFactor=0.5, seasonLength=0, valuesToForecast=1):
        """Initializes the HoltWintersMethod.

        :param Float smoothingFactor:    Defines the alpha for the Holt-Winters algorithm.
            Valid values are (0.0, 1.0).
        :param Float trendSmoothingFactor:    Defines the beta for the Holt-Winters algorithm..
            Valid values are (0.0, 1.0).
        :param Float seasonSmoothingFactor:    Defines the gamma for the Holt-Winters algorithm.
            Valid values are (0.0, 1.0). 
        :param Integer seasonLength:    The expected length for the seasons. Please use a good estimate here!
        :param Integer valuesToForecast:    Defines the number of forecasted values that will be part of the result.
        """
        super(HoltWintersMethod, self).__init__(["smoothingFactor",
                                          "trendSmoothingFactor",
                                          "seasonSmoothingFactor",
                                          "seasonLength"],
                                          valuesToForecast,
                                          True, True)

        if not 0 < seasonLength:
            raise ValueError("Please specify season length that is greater than 0.");

        self.set_parameter("smoothingFactor",      smoothingFactor)
        self.set_parameter("trendSmoothingFactor", trendSmoothingFactor)
        self.set_parameter("seasonSmoothingFactor", seasonSmoothingFactor)
        self.set_parameter("seasonLength",         seasonLength)

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

        parameterIntervals["smoothingFactor"]      = [0.0, 1.0, False, False]
        parameterIntervals["trendSmoothingFactor"] = [0.0, 1.0, False, False]
        parameterIntervals["seasonSmoothingFactor"] = [0.0, 1.0, False, False]

        return parameterIntervals

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values.

        :return:    TimeSeries object containing the exponentially smoothed TimeSeries,
            including the forecasted values.
        :rtype:     TimeSeries
        
        :note: Currently the first normalized value is simply chosen as the starting point.
        """
        ## determine the number of values to forecast, if necessary
        self._calculate_values_to_forecast(timeSeries)

        seasonLength = self.get_parameter("seasonLength")
        if len(timeSeries) < seasonLength:
            raise ValueError("The time series must contain at least one full season.")

        alpha = self.get_parameter("smoothingFactor")
        beta = self.get_parameter("trendSmoothingFactor")
        gamma = self.get_parameter("seasonSmoothingFactor")
        valuesToForecast = self._parameters["valuesToForecast"]


        seasonValues = self.initSeasonFactors(timeSeries)
        resultList = []
        lastEstimator = 0

        for idx in xrange(len(timeSeries)):
            t = timeSeries[idx][0]
            x_t = timeSeries[idx][1]
            if idx == 0:
                lastTrend = self.initialTrendSmoothingFactors(timeSeries)
                lastEstimator = x_t
                resultList.append([t, x_t])
                continue

            lastSeasonValue = seasonValues[idx % seasonLength]
            
            estimator = alpha * x_t/lastSeasonValue + (1 - alpha) * (lastEstimator + lastTrend)
            lastTrend = beta * (estimator - lastEstimator) + (1 - beta) * lastTrend
            seasonValues[idx % seasonLength] = gamma * x_t/estimator + (1 - gamma) * lastSeasonValue
            
            lastEstimator = estimator
            resultList.append([t, estimator])

        #Forecasting. Determine the time difference between two points for extrapolation
        currentTime        = resultList[-1][0]
        normalizedTimeDiff = currentTime - resultList[-2][0]
        
        for m in xrange(1, valuesToForecast + 1):
            currentTime += normalizedTimeDiff
            lastSeasonValue = seasonValues[(idx + m-1) % seasonLength]
            forecast = (lastEstimator + m * lastTrend) * lastSeasonValue
            resultList.append([currentTime, forecast])
        
        return TimeSeries.from_twodim_list(resultList)

    def initSeasonFactors(self, timeSeries):
        """ Computes the initial season smoothing factors.

        :return:    Returns a list of season vectors of length "seasonLength".
        :rtype:     List
        """

        seasonLength = self.get_parameter("seasonLength")
        try:
            seasonValues = self.get_parameter("seasonValues")
            assert seasonLength == len(seasonValues), "Preset Season Values have to have to be of season's length"
            return seasonValues
        except KeyError:
            pass

        seasonValues = []
        completeCycles = len(timeSeries) / seasonLength
        A = {} #cache values for A_j
        
        for i in xrange(seasonLength):
            c_i = 0
            for j in xrange(completeCycles):
                if j not in A:
                    A[j] = self.computeA(j, timeSeries)
                c_i += timeSeries[(seasonLength * j) + i][1] / A[j] #wikipedia suggests j-1, but we worked with indices in the first place
            c_i /= completeCycles
            seasonValues.append(c_i)
        return seasonValues

    def initialTrendSmoothingFactors(self, timeSeries):
        """ Calculate the initial Trend smoothing Factor b0.
        
        Explanation:
            http://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing

        :return:   Returns the initial trend smoothing factor b0
        """

        result = 0.0
        seasonLength = self.get_parameter("seasonLength")
        k = min(len(timeSeries) - seasonLength, seasonLength) #In case of only one full season, use average trend of the months that we have twice
        for i in xrange(0, k):
            result += (timeSeries[seasonLength + i][1] - timeSeries[i][1]) / seasonLength
        return result / k


    def computeA(self, j, timeSeries):
        """ Calculates A_j. Aj is the average value of x in the jth cycle of your data

        :return:    A_j
        :rtype:     Numeric
        """
        seasonLength = self.get_parameter("seasonLength")
        A_j = 0
        for i in range(seasonLength):
            A_j += timeSeries[(seasonLength * (j)) + i][1]
        return A_j / seasonLength
        ## :todo:
        #return A_j / float(seasonLength)
