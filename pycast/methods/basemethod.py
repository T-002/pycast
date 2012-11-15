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

from pycast.common.timeseries import TimeSeries

class BaseMethod(object):
    """Baseclass for all smoothing and forecasting methods."""

    _interval_definitions = { True: ["[", "]"], False: ["(", ")"]}

    def __init__(self, requiredParameters=[], hasToBeSorted=True, hasToBeNormalized=True):
        """Initializes the BaseMethod.

        @param requiredParameters List of parameternames that have to be defined.
        @param hasToBeSorted Defines if the TimeSeries has to be sorted or not.
        @param hasToBeNormalized Defines if the TimeSeries has to be normalized or not.
        """
        super(BaseMethod, self).__init__()
        self._parameters = {}
        self._parameterIntervals = self._get_parameter_intervals()

        self._requiredParameters = {}
        for entry in requiredParameters:
            self._requiredParameters[entry] = None

        self._hasToBeSorted     = hasToBeSorted
        self._hasToBeNormalized = hasToBeNormalized

    def _get_parameter_intervals(self):
        """Returns the intervals for the methods parameter.

        Only parameters with defined intervals can be used for optimization!

        @return Returns a dictionary containing the parameter intervals, using the parameter
                name as key, while the value hast the following format:
                [minValue, maxValue, minIntervalClosed, maxIntervalClosed]

                minValue:          Minimal value for the parameter
                maxValue:          Maximal value for the parameter
                minIntervalClosed: True, if minValue represents a valid value for the parameter.
                                   False otherwise.
                maxIntervalClosed: True, if maxValue represents a valid value for the parameter.
                                   False otherwise.
        """
        parameterIntervals = {}

        ## YOUR METHOD SPECIFIC CODE HERE!

        return parameterIntervals

    def get_interval(self, parameter):
        """Returns the interval for a given parameter.

        @param parameter Name of the parameter.

        @return Returns a list containing with [minValue, maxValue, minIntervalClosed, maxIntervalClosed].
                If no interval definitions for the given parameter exist, None is returned

                minValue:          Minimal value for the parameter
                maxValue:          Maximal value for the parameter
                minIntervalClosed: True, if minValue represents a valid value for the parameter.
                                   False otherwise.
                maxIntervalClosed: True, if maxValue represents a valid value for the parameter.
                                   False otherwise.
        """
        if not parameter in self._parameterIntervals:
            return None

        return self._parameterIntervals[parameter]

    def get_required_parameters(self):
        """Returns a list with the names of all required parameters.

        @return Returns a list with the names of all required parameters.
        """
        return self._requiredParameters.keys()

    def _in_valid_interval(self, parameter, value):
        """Returns if the parameter is within its valid interval.

        @param parameter Name of the parameter that has to be checked.
        @param value, value of the parameter.

        @return Returns True it the value for the given parameter is valid,
                        False otherwise.
        """
        ## return True, if not interval is defined for the parameter
        if not parameter in self._parameterIntervals:
            return True

        interval = self._parameterIntervals[parameter]

        if True == interval[2] and True == interval[3]:
            return interval[0] <= value <= interval[1]

        if False == interval[2] and True == interval[3]:
            return interval[0] <  value <= interval[1]

        if True == interval[2] and False == interval[3]:
            return interval[0] <= value <  interval[1]

        #if False == interval[2] and False == interval[3]:
        return interval[0] < value < interval[1]

    def _get_value_error_message_for_invalid_prarameter(self, parameter):
        """Returns the ValueError message for the given parameter.

        @param parameter Name of the parameter the message has to be created for.

        @return Returns a string containing hte message.
        """
        ## return if not interval is defined for the parameter
        if not parameter in self._parameterIntervals:
            return 

        interval = self._parameterIntervals[parameter]
        return "%s has to be in %s%s, %s%s." % (parameter, BaseMethod._interval_definitions[interval[2]][0], interval[0], interval[1], BaseMethod._interval_definitions[interval[3]][1])

    def set_parameter(self, name, value):
        """Sets a parameter for the BaseMethod.

        @param name Name of the parameter.
                             This should be a string.

        @param value Value of the parameter.
        """
        if not self._in_valid_interval(name, value):
            raise ValueError(self._get_value_error_message_for_invalid_prarameter(name))

        if name in self._parameters:
            print "Parameter %s already existed. It's old value will be replaced with %s" % (name, value)

        self._parameters[name] = value
    
    def get_parameter(self, name):
        """Returns a forecasting parameter.

        @param name Name of the parameter.

        @return Returns the value stored in parameter.

        @throw Throws a KeyError if the parameter is not defined.
        """
        return self._parameters[name]

    def has_to_be_normalized(self):
        """Returns if the TimeSeries has to be normalized or not.

        @return Returns True if the TimeSeries has to be normalized, False otherwise.
        """
        return self._hasToBeNormalized

    def has_to_be_sorted(self):
        """Returns if the TimeSeries has to be sorted or not.

        @return Returns True if the TimeSeries has to be sorted, False otherwise.
        """
        return self._hasToBeSorted

    def can_be_executed(self):
        """Returns if the method can already be executed.

        @return Returns True if all required parameters where already set, False otherwise.
        """
        missingParams = filter(lambda rp: rp not in self._parameters, self._requiredParameters)
        return len(missingParams) == 0

    def execute(self, timeSeries):
        """Executes the BaseMethod on a given TimeSeries object.

        @param timeSeries TimeSeries object that fullfills all requirements (normalization, sortOrder).

        @return Returns a TimeSeries object containing the smoothed/forecasted values.

        @throw Throws a NotImplementedError if the child class does not overwrite this function.
        """
        raise NotImplementedError
