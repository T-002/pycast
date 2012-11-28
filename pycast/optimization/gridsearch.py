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

from pycast.optimization import BaseOptimizationMethod

class GridSearch(BaseOptimizationMethod):
    """Implements the grid search method for parameter optimization. 

    GridSearch is the brute force method.
    """

    def optimize(self, timeSeries, forecastingMethods=[], startingPercentage=0.0, endPercentage=100.0):
        """Runs the optimization of the given TimeSeries.

        :param TimeSeries timeSeries:    TimeSeries instance that requires an optimized forecast.
        :param List forecastingMethods:    List of forecastingMethods that will be used for optimization.
        :param Float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started. 
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param Float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the vlaue, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.

        :return:    Returns the optimzed forecasting method, the corresponding error measure and the forecasting methods
            parameters.
        :rtype:     [BaseForecastingMethod, BaseErrorMeasure, Dictionary]

        :raise:    Raises a :py:exc:`ValueError` ValueError if no forecastingMethods is empty.
        """
        ## no forecasting methods provided
        if 0 == len(forecastingMethods):
            raise ValueError("forecastingMethods cannot be empty.")

        self._startingPercentage = startingPercentage
        self._endPercentage      = endPercentage

        results = []
        for forecastingMethod in forecastingMethods:
            results.append([forecastingMethod] + self.optimize_forecasting_method(timeSeries, forecastingMethod))

        ## get the forecasting method with the smallest error
        bestForecastingMethod = min(results, key=lambda item: item[1].get_error(self._startingPercentage, self._endPercentage))

        for parameter in bestForecastingMethod[2]:
            bestForecastingMethod[0].set_parameter(parameter, bestForecastingMethod[2][parameter])

        return bestForecastingMethod


    def _generate_next_parameter_value(self, parameter, forecastingMethod):
        """Generator for a specific parameter of the given forecasting method.

        :param String parameter:    Name of the parameter the generator is used for.
        :param BaseForecastingMethod forecastingMethod:    Instance of a ForecastingMethod.

        :return:    Creates a generator used to iterate over possible parameters.
        :rtype:     Generator Function
        """
        interval  = forecastingMethod.get_interval(parameter)
        precision = 10**self._precison

        startValue = interval[0]
        endValue   = interval[1]

        if not interval[2]:
            startValue += precision

        if interval[3]:
            endValue += precision

        while startValue < endValue:
            ## fix the parameter precision
            parameterValue = startValue
            
            yield parameterValue
            startValue += precision

    def optimize_forecasting_method(self, timeSeries, forecastingMethod):
        """Optimizes the parameters for the given timeSeries and forecastingMethod.

        :param TimeSeries timeSeries:    TimeSeries instance, containing hte original data.
        :param BaseForecastingMethod forecastingMethod:    ForecastingMethod that is used to optimize the parameters.

        :return: Returns a tuple containing only the smallest BaseErrorMeasure instance as defined in
            :py:meth:`BaseOptimizationMethod.__init__` and the forecastingMethods parameter.
        :rtype: Tuple
        """
        tuneableParameters = forecastingMethod.get_optimizable_parameters()

        remainingParameters = []
        for tuneableParameter in tuneableParameters:
            remainingParameters.append([tuneableParameter, [item for item in self._generate_next_parameter_value(tuneableParameter, forecastingMethod)]])

        ## Collect the forecasting results
        forecastingResults = self.optimization_loop(timeSeries, forecastingMethod, remainingParameters)

        ### Debugging GridSearchTest.inner_optimization_result_test
        #print ""
        #print "GridSearch"
        #print "Instance    /    SMAPE / Alpha"
        #for item in forecastingResults:
        #    print "%s / %s / %s" % (str(item[0])[-12:-1], str(item[0].get_error(self._startingPercentage, self._endPercentage))[:8], item[1]["smoothingFactor"])
        #print ""

        ## Collect the parameters that resulted in the smallest error
        bestForecastingResult = min(forecastingResults, key=lambda item: item[0].get_error(self._startingPercentage, self._endPercentage))

        ## return the determined parameters
        return bestForecastingResult

    def optimization_loop(self, timeSeries, forecastingMethod, remainingParameters, currentParameterValues={}):
        """The optimization loop.

        This function is called recursively, until all parameter values were evaluated.

        :param TimeSeries timeSeries:    TimeSeries instance that requires an optimized forecast.
        :param BaseForecastingMethod forecastingMethod:    ForecastingMethod that is used to optimize the parameters.
        :param list remainingParameters:    List containing all parameters with their corresponding values that still
            need to be evaluated.
            When this list is empty, the most inner optimization loop is reached.
        :param Dictionary currentParameterValues:    The currently evaluated forecast parameter combination.

        :return: Returns a list containing a BaseErrorMeasure instance as defined in
            :py:meth:`BaseOptimizationMethod.__init__` and the forecastingMethods parameter.
        :rtype: List
        """
        ## The most inner loop is reached
        if 0 == len(remainingParameters):
            ## set the forecasting parameters
            for parameter in currentParameterValues:
                forecastingMethod.set_parameter(parameter, currentParameterValues[parameter])

            ## calculate the forecast
            forecast = timeSeries.apply(forecastingMethod)

            ## create and initialize the ErrorMeasure
            error = self._errorClass(**self._errorMeasureKWArgs)

            ## when the error could not be calculated, return an empty result
            if not error.initialize(timeSeries, forecast):
                return []

            ## Debugging GridSearchTest.inner_optimization_result_test
            #print "Instance / SMAPE / Alpha: %s / %s / %s" % (str(error)[-12:-1], str(error.get_error(self._startingPercentage, self._endPercentage))[:8], currentParameterValues["smoothingFactor"])

            ## return the result
            return [[error, dict(currentParameterValues)]]
        
        ## If this is not the most inner loop than extract an additional parameter
        localParameter       = remainingParameters[-1]
        localParameterName   = localParameter[0]
        localParameterValues = localParameter[1]


        ## initialize the result
        results = []
        
        ## check the next level for each existing parameter
        for value in localParameterValues:
            currentParameterValues[localParameterName] = value
            remainingParameters = remainingParameters[:-1]
            results += self.optimization_loop(timeSeries, forecastingMethod, remainingParameters, currentParameterValues)

        return results