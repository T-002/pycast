#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Copyright (c) 2012-2015 Christian Schwarz
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

## TimeSeries related tests
from timeseriesdatabasetest         import DatabaseConnectorTest
from timeseriesmiscellaneoustest    import TimeSeriesMiscellaneousTest
from json_encodertest               import PycastEncoderTest
from multidimensionaltimeseriestest import MultiDimensionalTimeSeriesTest

## profileMe decorator related tests
from profilemetest import ProfileMeDecoratorTest

## helper tests
from helpertest import HelperTest

## method tests
from methodtest import BaseMethodTest, BaseForecastingMethodTest, SimpleMovingAverageTest, ExponentialSmoothingTest, HoltMethodTest, HoltWintersMethodTest
from regressiontest import RegressionTest, LinearRegressionTest

## error measure tests
from errormeasuretest import BaseErrorMeasureTest
from meansquarederrortest import MeanSquaredErrorTest
from symmetricmeanabsolutepercentageerrortest import SymmetricMeanAbsolutePercentageErrorTest
from meanabsolutedeviationerrortest import MeanAbsoluteDeviationErrorTest
from medianabsolutepercentageerrortest import MedianAbsolutePercentageErrorTest
from meanabsolutescalederrortest import MeanAbsoluteScaledErrorTest
from meansigneddifferenceerrortest import MeanSignedDifferenceErrorTest
from meanabsolutepercentageerrortest import MeanAbsolutePercentageErrorTest
from geometricmeanabsolutepercentageerrortest import GeometricMeanAbsolutePercentageErrorTest
from meansignedpercentageerrortest import MeanSignedPercentageErrorTest
from weightedmapetest import WeightedMeanAbsolutePercentageErrorTest
#from meetest import MeanEconomicErrorTest

## optimization method
from baseoptimizationtest import BaseOptimizationMethodTest
from gridsearchtest       import GridSearchTest

#decorators test
from decoratorstest import OptimizedDecoratorTest

# matrix test
from matrixtest import MatrixTest, VectorTest, MatrixHelperTest
