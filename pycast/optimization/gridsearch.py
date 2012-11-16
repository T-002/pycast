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

        @param timeSeries TimeSeries instance that requires an optimized forecast. It has to have
        @params forecastingMethods List of forecastingMethods that will be used for optimization.
                This list cannot be empty!

        @return Returns the optimzed forecasting method with the smallest error.

        @throw ValueError Throws a ValueError if no forecastingMethods are defined.
        """
        ## no forecasting methods provided
        if 0 == len(forecastingMethods):
            raise ValueError("forecastingMethods cannot be empty.")

    def _generate_next_parameter_value(self, parameter, forecastingMethod):
        """Generator for a specific parameter of the given forecasting method.

        @param parameter Name of the parameter the generator is used for.
        @param forecastingMethod Instance of a ForecastingMethod.

        @return Creates a generator used to iterate over possible parameters.
        """
        interval = forecastingMethod.get_interval(parameter)
        precision = self._precison

        startValue = interval[0]
        endValue   = interval[1]

        if not interval[2]:
            startValue += precision

        if interval[3]:
            endValue += precision

        for value in xrange(startValue, endValue, precision):
            yield value

    def optimize_forecasting_method(self, timeSeries, forecastingMethod):
        """Optimizes the parameters for the given timeSeries and forecastingMethod.

        @param timeSeries TimeSeries instance, containing hte original data.
        @param forecastingMethod ForecastingMethod that is used to optimize the parameters.

        @todo Missing: - Errorclass for calculation
                       - percentage for start_error_measure, end_error_measure
                       - Definition of the result that will be returned.
        """
        raise NotImplementedError
        
        tuneableParameters = forecastingMethod.get_required_parameters()

        generators = {}
        for tuneableParameter in tuneableParameters:
            generators[tuneableParameter] = self._generate_next_parameter_value(parameter, forecastingMethod)