# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# Copyright (c) 2012-2015 Christian Schwarz
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import types

from pycast.errors.baseerrormeasure import BaseErrorMeasure

from pycast.common.pycastobject import PyCastObject
class BaseOptimizationMethod(PyCastObject):

    """Baseclass for all optimization methods."""

    def __init__(self, errorMeasureClass, errorMeasureInitializationParameters=None, precision=-1):
        """Initializes the optimization method.

        :param BaseErrorMeasure errorMeasureClass:    Error measure class from :py:mod:`pycast.errors`.
        :param dictionary errorMeasureInitializationParameters:    Parameters used to initialize
            the errorMeasureClass. This dictionary will be passed to the errorMeasureClass as \*\*kwargs.
        :param integer precision:    Defines the accuracy for parameter tuning in 10^precision.
            This parameter has to be an integer in [-7, 0].

        :raise:    Raises a :py:exc:`TypeError` if errorMeasureClass is not a valid class.
            Valid classes are derived from :py:class:`pycast.errors.BaseErrorMeasure`.
        :raise:    Raises a :py:exc:`ValueError` if precision is not in [-7, 0].
        """

        if errorMeasureInitializationParameters is None:
            errorMeasureInitializationParameters = {}

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

    def optimize(self, timeSeries, forecastingMethods=None, startingPercentage=0.0, endPercentage=100.0):
        """Runs the optimization on the given TimeSeries.

        :param TimeSeries timeSeries:    TimeSeries instance that requires an optimized forecast.
        :param list forecastingMethods:    List of forecastingMethods that will be used for optimization.
        :param float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started.
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.


        :return:    Returns the optimized forecasting method with the smallest error.
        :rtype:     (BaseForecastingMethod, Dictionary)

        :raise:    Raises a :py:exc:`ValueError` ValueError if no forecastingMethods is empty.
        """
        # no forecasting methods provided
        if forecastingMethods is None or len(forecastingMethods) == 0:
            raise ValueError("forecastingMethods cannot be empty.")