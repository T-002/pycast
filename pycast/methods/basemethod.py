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

        :param List requiredParameters:    List of parameternames that have to be defined.
        :param Boolean hasToBeSorted:    Defines if the TimeSeries has to be sorted or not.
        :param Boolean hasToBeNormalized:    Defines if the TimeSeries has to be normalized or not.
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

        ## YOUR METHOD SPECIFIC CODE HERE!
        if self.__class__.__name__ not in ["BaseMethod", "BaseForecastingMethod"]:
            raise NotImplementedError

        return parameterIntervals

    def get_interval(self, parameter):
        """Returns the interval for a given parameter.

        :param String parameter:     Name of the parameter.

        :return:     Returns a list containing with [minValue, maxValue, minIntervalClosed, maxIntervalClosed].
            If no interval definitions for the given parameter exist, :py:const:`None` is returned.

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
        :rtype:    List
        """
        if not parameter in self._parameterIntervals:
            return None

        return self._parameterIntervals[parameter]

    def get_required_parameters(self):
        """Returns a list with the names of all required parameters.

        :return:    Returns a list with the names of all required parameters.
        :rtype:     List
        """
        return self._requiredParameters.keys()

    def _in_valid_interval(self, parameter, value):
        """Returns if the parameter is within its valid interval.

        :param String parameter:     Name of the parameter that has to be checked.
        :param Numeric value:     Value of the parameter.

        :return:    Returns :py:const:`True` it the value for the given parameter is valid,
            :py:const:`False` otherwise.
        :rtype:     Boolean
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

    def _get_value_error_message_for_invalid_prarameter(self, parameter, value):
        """Returns the ValueError message for the given parameter.

        :param String parameter:    Name of the parameter the message has to be created for.
        :param Numeric value:    Value outside the parameters interval.

        :return:    Returns a string containing hte message.
        :rtype:     String
        """
        ## return if not interval is defined for the parameter
        if not parameter in self._parameterIntervals:
            return 

        interval = self._parameterIntervals[parameter]
        return "%s has to be in %s%s, %s%s. Current value is %s." % (parameter, BaseMethod._interval_definitions[interval[2]][0], interval[0], interval[1], BaseMethod._interval_definitions[interval[3]][1], value)

    def set_parameter(self, name, value):
        """Sets a parameter for the BaseMethod.

        :param String name:     Name of the parameter that has to be checked.
        :param Numeric value:     Value of the parameter.
        """
        if not self._in_valid_interval(name, value):
            raise ValueError(self._get_value_error_message_for_invalid_prarameter(name, value))

        #if name in self._parameters:
        #    print "Parameter %s already existed. It's old value will be replaced with %s" % (name, value)

        self._parameters[name] = value
    
    def get_parameter(self, name):
        """Returns a forecasting parameter.

        :param String name:    Name of the parameter.

        :return:    Returns the value stored in parameter.
        :rtype:     Numeric

        :raise:    Raises a :py:exc:`KeyError` if the parameter is not defined.
        """
        return self._parameters[name]

    def has_to_be_normalized(self):
        """Returns if the TimeSeries has to be normalized or not.

        :return:    Returns :py:const:`True` if the TimeSeries has to be normalized, :py:const:`False` otherwise.
        :rtype:     Boolean
        """
        return self._hasToBeNormalized

    def has_to_be_sorted(self):
        """Returns if the TimeSeries has to be sorted or not.

        :return:    Returns :py:const:`True` if the TimeSeries has to be sorted, :py:const:`False` otherwise.
        :rtype:     Boolean
        """
        return self._hasToBeSorted

    def can_be_executed(self):
        """Returns if the method can already be executed.

        :return:    Returns :py:const:`True` if all required parameters where already set, False otherwise.
        :rtype:     Boolean 
        """
        missingParams = filter(lambda rp: rp not in self._parameters, self._requiredParameters)
        return len(missingParams) == 0

    def execute(self, timeSeries):
        """Executes the BaseMethod on a given TimeSeries object.

        :param TimeSeries timeSeries: TimeSeries object that fullfills all requirements (normalization, sortOrder).

        :return:    Returns a TimeSeries object containing the smoothed/forecasted values.
        :rtype:     TimeSeries

        :raise:    Raises a :py:exc:`NotImplementedError` if the child class does not overwrite this function.
        """
        raise NotImplementedError

class BaseForecastingMethod(BaseMethod):
    """Basemethod for all forecasting methods."""

    def __init__(self, requiredParameters=[], valuesToForecast=1, hasToBeSorted=True, hasToBeNormalized=True):
        """Initializes the BaseForecastingMethod.

        :param List requiredParameters:    List of parameternames that have to be defined.
        :param Integer valuesToForecast:    Number of entries that will be forecasted.
            This can be changed by using forecast_until().
        :param Boolean hasToBeSorted:    Defines if the TimeSeries has to be sorted or not.
        :param Boolean hasToBeNormalized:    Defines if the TimeSeries has to be normalized or not.

        :raise: Raises a :py:exc:`ValueError` when valuesToForecast is smaller than zero.
        """
        if not "valuesToForecast" in requiredParameters:
            requiredParameters.append("valuesToForecast")
        if valuesToForecast < 0:
            raise ValueError("valuesToForecast has to be larger than zero.")

        super(BaseForecastingMethod, self).__init__(requiredParameters, hasToBeSorted=hasToBeSorted, hasToBeNormalized=hasToBeNormalized)

        self.set_parameter("valuesToForecast", valuesToForecast)

        self._forecastUntil = None

    def get_optimizable_parameters(self):
        """Returns a list with optimizable parameters.

        All required parameters of a forecasting method with defined intervals can be used for optimization.

        :return:    Returns a list with optimizable parameter names.
        :rtype:     List

        :todo:    Should we return all parameter names from the self._parameterIntervals instead?
        """
        return filter(lambda parameter: parameter in self._parameterIntervals, self._requiredParameters)

    def set_parameter(self, name, value):
        """Sets a parameter for the BaseForecastingMethod.

        :param String name:    Name of the parameter.
        :param Numeric value:    Value of the parameter.
        """
        ## set the furecast until variable to None if necessary
        if name == "valuesToForecast":
            self._forecastUntil = None

        ## continue with the parents implementation
        return super(BaseForecastingMethod, self).set_parameter(name, value)

    def forecast_until(self, timestamp, format=None):
        """Sets the forecasting goal (timestamp wise).

        This function enables the automatic determination of valuesToForecast.

        :param timestamp:    timestamp containing the end date of the forecast.
        :param String format:    Format of the timestamp. This is used to convert the
            timestamp from UNIX epochs, if necessary. For valid examples
            take a look into the :py:func:`time.strptime` documentation.
        """
        if None != format:
            timestamp = TimeSeries.convert_timestamp_to_epoch(timestamp, format)

        self._forecastUntil = timestamp

    def _calculate_values_to_forecast(self, timeSeries):
        """Calculates the number of values, that need to be forecasted to match the goal set in forecast_until.

        This sets the parameter "valuesToForecast" and should be called at the beginning of the :py:meth:`BaseMethod.execute` implementation.

        :param TimeSeries timeSeries:    Should be a sorted and normalized TimeSeries instance.

        :raise:    Raises a :py:exc:`ValueError` if the TimeSeries is either not normalized or sorted.
        """
        ## do not set anything, if it is not required
        if None == self._forecastUntil:
            return

        ## check the TimeSeries for correctness
        if not timeSeries.is_sorted():
            raise ValueError("timeSeries has to be sorted.")
        if not timeSeries.is_normalized():
            raise ValueError("timeSeries has to be normalized.")

        timediff = timeSeries[-1][0] - timeSeries[-2][0]
        forecastSpan = self._forecastUntil - timeSeries[-1][0]

        self.set_parameter("valuesToForecast", int(forecastSpan / timediff) + 1)