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

## the mother of all errors
from baseerrormeasure import BaseErrorMeasure

## absolute errors
from meansquarederror                     import MeanSquaredError, MSE
from meanabsolutedeviationerror           import MeanAbsoluteDeviationError, MAD
from meansigneddifferenceerror            import MeanSignedDifferenceError, MSD

## scaled errors that can be used to compare prediction accuracy on different TimeSeries
from meanabsolutepercentageerror          import MeanAbsolutePercentageError, MAPE
from geometricmeanabsolutepercentageerror import GeometricMeanAbsolutePercentageError, GMAPE
from meansignedpercentageerror            import MeanSignedPercentageError, MSPE
from symmetricmeanabsolutepercentageerror import SymmetricMeanAbsolutePercentageError, SMAPE
from medianabsolutepercentageerror        import MedianAbsolutePercentageError, MdAPE
from weightedmeanabsolutepercentageerror  import WeightedMeanAbsolutePercentageError, WMAPE
from meanabsolutescalederror              import MeanAbsoluteScaledError, MASE


#from meaneconomicerror           import MeanEconomicError, MEE, MeanSignedEconomicError, MSEE
