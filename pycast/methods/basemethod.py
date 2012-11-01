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

    def __init__(self, requiredParameters, hasToBeSorted=True, hasToBeNormalized=True):
        """Initializes the BaseMethod.

        @param requiredParameters List of parameternames that have to be defined.

        @param sorted Defines if the TimeSeries has to be sorted or not.

        @param normalized Defines if the TimeSeries has to be normalized or not.
        """
        super(BaseMethod, self).__init__()
        self._parameters = {}

        self._requiredParameters = {}
        for entry in requiredParameters:
            self._requiredParameters[entry] = None

        self._hasToBeSorted     = hasToBeSorted
        self._hasToBeNormalized = hasToBeNormalized

    def add_parameter(self, name, value):
        """Adds a parameter for the BaseMethod.

        @param name Name of the parameter.
                             This should be a string.

        @param value Value of the parameter.
        """
        if name in self._parameters:
            print "Parameter %s already existed. It's old value will be replaced with %s" % (name, value)

        self._parameters[name] = value

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
        """
        raise NotImplementedError
