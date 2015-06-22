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

from pycast.common.pycastobject import PyCastObject
from pycast.common.timeseries import TimeSeries, FusionMethods
from pycast.errors.meansigneddifferenceerror import MSD

class Regression(PyCastObject):

    def __init__(self):
        """Initializes the Regression."""
        super(Regression, self).__init__()

    def calculate_parameters(self, independentTs, dependentTs):
        """Calculate and return the parameters for the regression line

        Return the parameter for the line describing the relationship
        between the input variables.

        :param Timeseries independentTs: The Timeseries used for the
            independent variable (x-axis). The Timeseries must have
            at least 2 datapoints with different dates and values
        :param Timeseries dependentTs: The Timeseries used as the
            dependent variable (y-axis). The Timeseries must have
            at least 2 datapoints, which dates match with independentTs

        :return:    A tuple containing the y-axis intercept and the slope
                    used to execute the regression
        :rtype:     tuple
        :raise: Raises an :py:exc:`ValueError` if
                - independentTs and dependentTs have not at least two matching dates
                - independentTs has only one distinct value
                - The dates in one or both Timeseries are not distinct.
        """
        listX, listY = self.match_time_series(independentTs, dependentTs)

        if len(listX) == 0 or len(listY) == 0:
            raise ValueError("Lists need to have some equal dates or cannot be empty")
        if len(listX) != len(listY):
            raise ValueError("Each Timeseries need to have distinct dates")

        xValues = map(lambda item: item[1], listX)
        yValues = map(lambda item: item[1], listY)

        xMean = FusionMethods["mean"](xValues)
        yMean = FusionMethods["mean"](yValues)

        xDeviation = map(lambda item: (item - xMean), xValues)
        yDeviation = map(lambda item: (item - yMean), yValues)

        try:
            parameter1 = sum(x * y for x, y in zip(xDeviation, yDeviation)) / sum(x * x for x in xDeviation)
        except ZeroDivisionError:
            ## error occures if xDeviation is always 0, which means that all x values are the same
            raise ValueError("Not enough distinct x values")
        parameter0 = yMean - (parameter1 * xMean)

        return (parameter0, parameter1)

    def calculate_parameters_with_confidence(self, independentTs, dependentTs, confidenceLevel, samplePercentage=.1):
        """Same functionality as calculate_parameters, just that additionally
        the confidence interval for a given confidenceLevel is calculated.
        This is done based on a sample of the dependentTs training data that is validated
        against the prediction. The signed error of the predictions and the sample is then
        used to calculate the bounds of the interval.

        further reading: http://en.wikipedia.org/wiki/Confidence_interval

        :param Timeseries independentTs: The Timeseries used for the
            independent variable (x-axis). The Timeseries must have
            at least 2 datapoints with different dates and values
        :param Timeseries dependentTs: The Timeseries used as the
            dependent variable (y-axis). The Timeseries must have
            at least 2 datapoints, which dates match with independentTs
        :param float confidenceLevel: The percentage of entries in the sample that should
            have an prediction error closer or equal to 0 than the bounds of the confidence interval.
        :param float samplePercentage: How much of the dependentTs should be used for sampling

        :return:    A tuple containing the y-axis intercept and the slope
                    used to execute the regression and the (underestimation, overestimation)
                    for the given confidenceLevel
        :rtype:     tuple
        :raise: Raises an :py:exc:`ValueError` if
                - independentTs and dependentTs have not at least two matching dates
                - independentTs has only one distinct value
                - The dates in one or both Timeseries are not distinct.
        """
        #First split the time series into sample and training data
        sampleY, trainingY = dependentTs.sample(samplePercentage)

        sampleX_list = self.match_time_series(sampleY, independentTs)[1]
        trainingX_list = self.match_time_series(trainingY, independentTs)[1]

        sampleX = TimeSeries.from_twodim_list(sampleX_list)
        trainingX = TimeSeries.from_twodim_list(trainingX_list)

        #Then calculate parameters based on the training data
        n, m = self.calculate_parameters(trainingX, trainingY)

        #predict
        prediction = self.predict(sampleX, n, m)

        #calculate the signed error at each location, note that MSD(x,y) != MSD(y,x)
        msd = MSD()
        msd.initialize(prediction, sampleY)

        return (n, m, msd.confidence_interval(confidenceLevel))

    def predict(self, timeseriesX, n, m):
        """
        Calculates the dependent timeseries Y for the given parameters
        and independent timeseries. (y=m*x + n)

        :param TimeSeries timeseriesX: the independent Timeseries.

        :param float n: The interception with the x access
            that has been calculated during regression

        :param float m: The slope of the function
            that has been calculated during regression

        :return TimeSeries timeseries_y: the predicted values for the
            dependent TimeSeries. Its length and first dimension will
            equal to timeseriesX.
        """
        new_entries = []
        for entry in timeseriesX:
            predicted_value = m * entry[1] + n
            new_entries.append([entry[0], predicted_value])
        return TimeSeries.from_twodim_list(new_entries)

    def match_time_series(self, timeseries1, timeseries2):
        """Return two lists of the two input time series with matching dates

        :param TimeSeries timeseries1: The first timeseries
        :param TimeSeries timeseries2: The second timeseries
        :return:    Two two dimensional lists containing the matched values,
        :rtype:     two List
        """
        time1 = map(lambda item: item[0], timeseries1.to_twodim_list())
        time2 = map(lambda item: item[0], timeseries2.to_twodim_list())

        matches = filter(lambda x: (x in time1), time2)
        listX  = filter(lambda x: (x[0] in matches), timeseries1.to_twodim_list())
        listY  = filter(lambda x: (x[0] in matches), timeseries2.to_twodim_list())

        return listX, listY


class LinearRegression(PyCastObject):

    @classmethod
    def lstsq(cls, a, b):
        """Return the least-squares solution to a linear matrix equation.

        :param Matrix a:    Design matrix with the values of the independent variables.
        :param Matrix b:    Matrix with the "dependent variable" values.
                            b can only have one column.

        :raise:             Raises an :py:exc:`ValueError`, if
                            - the number of rows of a and b does not match.
                            - b has more than one column.
        :note:              The algorithm solves the following equations.
                            beta = a^+ b.
        """
        # Check if the size of the input matrices matches
        if a.get_height() != b.get_height():
            raise ValueError("Size of input matrices does not match")
        if b.get_width() != 1:
            raise ValueError("Matrix with dependent variable has more than 1 column")
        aPseudo = a.pseudoinverse()
        # The following code could be used if c is regular.
        # aTrans  = a.transform()
        # c       = aTrans * a
        # invers() raises an ValueError, if c is not invertible
        # cInvers = c.invers()
        # beta = cInvers * aTrans * b
        beta = aPseudo * b
        return beta
