#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Copyright (c) 2012-2013 Christian Schwarz
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

from pycast.common import PyCastObject
from pycast.common.decorators import optimized

class BaseErrorMeasure(PyCastObject):
    """Baseclass for all error measures."""

    def __init__(self, minimalErrorCalculationPercentage=60):
        """Initializes the error measure.

        :param Integer minimalErrorCalculationPercentage:    The number of entries in an
            original TimeSeries that have to have corresponding partners in the calculated
            TimeSeries. Corresponding partners have the same time stamp.
            Valid values are in [0.0, 100.0].

        :raise: Raises a :py:exc:`ValueError` if minimalErrorCalculationPercentage is not
            in [0.0, 100.0].
        """
        super(BaseErrorMeasure, self).__init__()

        if not 0.0 <= minimalErrorCalculationPercentage <= 100.0:
            raise ValueError("minimalErrorCalculationPercentage has to be in [0.0, 100.0].")

        self._minimalErrorCalculationPercentage = minimalErrorCalculationPercentage / 100.0
        
        self._errorValues = []
        self._errorDates  = []

    @optimized
    def initialize(self, originalTimeSeries, calculatedTimeSeries):
        """Initializes the ErrorMeasure.

        During initialization, all :py:meth:`BaseErrorMeasure.local_errors` are calculated.

        :param TimeSeries originalTimeSeries:    TimeSeries containing the original data.
        :param TimeSeries calculatedTimeSeries:    TimeSeries containing calculated data.
            Calculated data is smoothed or forecasted data.

        :return:    Return :py:const:`True` if the error could be calculated, :py:const:`False`
            otherwise based on the minimalErrorCalculationPercentage.
        :rtype:     Boolean

        :raise:    Raises a :py:exc:`StandardError` if the error measure is initialized multiple times.
        """
        ## ErrorMeasure was already initialized.
        if 0 < len(self._errorValues):
            raise StandardError("An ErrorMeasure can only be initialized once.")
        
        ## sort the TimeSeries to reduce the required comparison operations
        originalTimeSeries.sort_timeseries()
        calculatedTimeSeries.sort_timeseries()
        
        ## Performance optimization
        append      = self._errorValues.append
        appendDate  = self._errorDates.append
        local_error = self.local_error

        minCalcIdx  = 0

        ## calculate all valid local errors
        for orgPair in originalTimeSeries:
            for calcIdx in xrange(minCalcIdx, len(calculatedTimeSeries)):
                calcPair = calculatedTimeSeries[calcIdx]

                ## Skip values that can not be compared
                if calcPair[0] != orgPair[0]:
                    continue

                append(local_error(orgPair[1:], calcPair[1:]))
                appendDate(orgPair[0])

        ## return False, if the error cannot be calculated
        if len(filter(lambda item: item != None, self._errorValues)) < self._minimalErrorCalculationPercentage * len(originalTimeSeries):
            self._errorValues = []
            self._errorDates = []
            return False

        return True

    def _get_error_values(self, startingPercentage, endPercentage, startDate, endDate):
        """Gets the defined subset of self._errorValues.

        Both parameters will be correct at this time.

        :param Float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started. 
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param Float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the vlaue, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.
        :param Float startDate: Epoch representing the start date used for error calculation.
        :param Float endDate: Epoch representing the end date used in the error calculation.

        :return:    Returns a list with the defined error values.
        :rtype:     List

        :raise:    Raises a ValueError if startDate or endDate do not represent correct boundaries for error calculation.
        """
        if None != startDate:
            possibleDates = filter(lambda date: date >= startDate, self._errorDates)
            if 0 == len(possibleDates):
                raise ValueError("%s does not represent a valid startDate." % startDate)
            
            startIdx = self._errorDates.index(min(possibleDates))
        else:
            startIdx = int((startingPercentage * len(self._errorValues)) / 100.0)

        if None != endDate:
            possibleDates = filter(lambda date: date <= endDate, self._errorDates)
            if 0 == len(possibleDates):
                raise ValueError("%s does not represent a valid endDate." % endDate)

            endIdx = self._errorDates.index(max(possibleDates)) + 1
        else:
            endIdx = int((endPercentage * len(self._errorValues)) / 100.0)

        return self._errorValues[startIdx:endIdx]

    def get_error(self, startingPercentage=0.0, endPercentage=100.0, startDate=None, endDate=None):
        """Calculates the error for the given interval (startingPercentage, endPercentage) between the TimeSeries 
        given during :py:meth:`BaseErrorMeasure.initialize`.

        :param Float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started. 
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param Float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the vlaue, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.
        :param Float startDate: Epoch representing the start date used for error calculation.
        :param Float endDate: Epoch representing the end date used in the error calculation.

        :return:    Returns a float representing the error.
        :rtype:     Float

        :raise:    Raises a :py:exc:`ValueError` in one of the following cases:
            
            - startingPercentage not in [0.0, 100.0]
            - endPercentage      not in [0.0, 100.0]
            - endPercentage < startingPercentage

        :raise:    Raises a :py:exc:`StandardError` if :py:meth:`BaseErrorMeasure.initialize` was not successfull before.
        """
        ## not initialized:
        if len(self._errorValues) == 0:
            raise StandardError("The last call of initialize(...) was not successfull.")

        ## check for wrong parameters
        if not (0.0 <= startingPercentage <= 100.0):
            raise ValueError("startingPercentage has to be in [0.0, 100.0].")
        if not (0.0 <= endPercentage <= 100.0):
            raise ValueError("endPercentage has to be in [0.0, 100.0].")
        if endPercentage < startingPercentage:
            raise ValueError("endPercentage has to be greater or equal than startingPercentage.")

        return self._calculate(startingPercentage, endPercentage, startDate, endDate)
    
    def _calculate(self, startingPercentage, endPercentage, startDate, endDate):
        """This is the error calculation function that gets called by :py:meth:`BaseErrorMeasure.get_error`.

        Both parameters will be correct at this time.

        :param Float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started. 
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param Float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the vlaue, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.
        :param Float startDate: Epoch representing the start date used for error calculation.
        :param Float endDate: Epoch representing the end date used in the error calculation.

        :return:    Returns a float representing the error.
        :rtype:     Float

        :raise:    Raises a :py:exc:`NotImplementedError` if the child class does not overwrite this method.
        """
        raise NotImplementedError


    def local_error(self, originalValue, calculatedValue):
        """Calculates the error between the two given values.

        :param List originalValue:    List containing the values of the original data.
        :param List calculatedValue:    List containing the values of the calculated TimeSeries that
            corresponds to originalValue.

        :return:    Returns the error measure of the two given values.
        :rtype:     Numeric

        :raise:    Raises a :py:exc:`NotImplementedError` if the child class does not overwrite this method.
        """
        raise NotImplementedError

    def confidence_interval(self, confidenceLevel):
        """Calculates for which value confidenceLevel% of the errors are closer to 0.

        :param float confidenceLevel: percentage of the errors that should be
            smaller than the returned value for overestimations and larger than
            the returned value for underestimations.
            confidenceLevel has to be in [0.0, 1.0]

        :return:    return a tuple containing the underestimation and overestimation for
            the given confidenceLevel
        :rtype:     tuple

        :warning:    Index is still not calculated correctly
        """

        if not (confidenceLevel >= 0 and confidenceLevel <= 1):
            raise ValueError("Parameter percentage has to be in [0,1]")

        underestimations = []
        overestimations = []
        for error in self._errorValues:
            if error is None:
                # None was in the lists causing some confidenceLevels not be calculated, not sure if that was intended, I suggested ignoring None values
                continue
            #Want 0 errors in both lists!
            if error >= 0:
                overestimations.append(error)
            if error <= 0:
                underestimations.append(error)

        #sort and cut off at confidence level.
        overestimations.sort()
        underestimations.sort(reverse=True)

        overIdx  = int(len(overestimations) * confidenceLevel) - 1
        underIdx = int(len(underestimations) * confidenceLevel) - 1
        
        overestimation  = 0.0
        underestimation = 0.0

        if overIdx >= 0:
            overestimation = overestimations[overIdx]
        else:
            print len(overestimations), confidenceLevel

        if underIdx >= 0:
            underestimation = underestimations[underIdx]

        return underestimation, overestimation
