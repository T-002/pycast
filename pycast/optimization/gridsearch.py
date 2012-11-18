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

    def optimize(self, timeSeries, forecastingMethods=[]):
        """Runs the optimization of the given TimeSeries.

        :param TimeSeries timeSeries:    TimeSeries instance that requires an optimized forecast.
        :param List forecastingMethods:    List of forecastingMethods that will be used for optimization.

        :return:    Returns the optimzed forecasting method with the smallest error.
        :rtype:     BaseForecastingMethod, Dictionary

        :raise:    Raises a :py:exc:`ValueError` ValueError if no forecastingMethods is empty.
        """
        ## no forecasting methods provided
        if 0 == len(forecastingMethods):
            raise ValueError("forecastingMethods cannot be empty.")

        bestForecastingMethod = None
        bestParameters        = None

        for forecastingMethod in forecastingMethods:
            parameters = self.optimize_forecasting_method(timeSeries, forecastingMethod)

        return bestForecastingMethod, parameters

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
            yield startValue
            startValue += precision

    def optimize_forecasting_method(self, timeSeries, forecastingMethod):
        """Optimizes the parameters for the given timeSeries and forecastingMethod.

        :param TimeSeries timeSeries:    TimeSeries instance, containing hte original data.
        :param BaseForecastingMethod forecastingMethod:    ForecastingMethod that is used to optimize the parameters.

        :todo:    Errorclass for calculation
        :todo:    percentage for start_error_measure, end_error_measure
        :todo:    Definition of the result that will be returned.
        """
        tuneableParameters = forecastingMethod.get_optimizable_parameters()

        generators = {}
        for tuneableParameter in tuneableParameters:
            generators[tuneableParameter] = self._generate_next_parameter_value(tuneableParameter, forecastingMethod)

        parameters = {}
        for parameter in tuneableParameters:
            parameters[parameter] = None

        smallestError = None

        ## do the loop magic here....
        ### one for loop for each parameter
        #### in the most inner loop, the currently chosen parameters should be stored if the calculated error is smaller
        #### than the last smallestError.
        ####
        #### parameters should contain the parameter values that resulted in the smalles error.

        return parameters