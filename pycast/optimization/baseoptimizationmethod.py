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

import types 

from pycast.errors import BaseErrorMeasure

class BaseOptimizationMethod(object):
    """Baseclass for all optimization methods."""

    def __init__(self, errorMeasureClass, errorMeasureInitializationParameters={}, precision=-1):
        """Initializes the optimization method.

        :param BaseErrorMeasure errorMeasureClass:    Error measure class from :py:mod:`pycast.errors`.
        :param Dictionary errorMeasureInitializationParameters:    Parameters used to initialize
            the errorMeasureClass. This dictionary will be passed to the errorMeasureClass as \*\*kwargs.
        :param Integer precision:    Defines the accuracy for parameter tuning in 10^precision.
            This parameter has to be an integer in [-7, 0].

        :raise:    Raises a :py:exc:`TypeError` if errorMeasureClass is not a valid class.
            Valid classes are derived from :py:class:`pycast.errors.BaseErrorMeasure`.
        :raise:    Raises a :py:exc:`ValueError` if precision is not in [-7, 0].
        """
        if not isinstance(errorMeasureClass, (type, types.ClassType)):
            raise TypeError("errorMeasureClass has to be of type pycast.errors.BaseErrorMeasure or of an inherited class.")
        if not issubclass(errorMeasureClass, BaseErrorMeasure):
            raise TypeError("errorMeasureClass has to be of type pycast.errors.BaseErrorMeasure or of an inherited class.")
        if not -7 <= precision <= 0:
            raise ValueError("precision has to be in [-7,0].")

        super(BaseOptimizationMethod, self).__init__()

        self._precison   = int(precision)
        self._errorClass = errorMeasureClass
        self._errorMeasureKWArgs = errorMeasureInitializationParameters

    def optimize(self, timeSeries, forecastingMethods=[]):
        """Runs the optimization on the given TimeSeries.

        :param TimeSeries timeSeries:    TimeSeries instance that requires an optimized forecast.
        :param List forecastingMethods:    List of forecastingMethods that will be used for optimization.

        :return:    Returns the optimzed forecasting method with the smallest error.
        :rtype:     (BaseForecastingMethod, Dictionary)

        :raise:    Raises a :py:exc:`ValueError` ValueError if no forecastingMethods is empty.
        """
        ## no forecasting methods provided
        if 0 == len(forecastingMethods):
            raise ValueError("forecastingMethods cannot be empty.")