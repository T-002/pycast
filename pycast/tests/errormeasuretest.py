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

## required external modules
import unittest

## required modules from pycast
from pycast.errors import BaseErrorMeasure
from pycast.errors import MeanSquaredError
from pycast.errors import SymmetricMeanAbsolutePercentageError
from pycast.errors import MeanAbsoluteDeviationError
from pycast.errors import MeanAbsoluteScaledError
from pycast.errors import MedianAbsolutePercentageError
from pycast.common.timeseries import TimeSeries

class BaseErrorMeasureTest(unittest.TestCase):
    """Test class for the BaseErrorMeasure interface."""

    def initialization_test(self):
        """Test the BaseErrorMeasure initialization."""
        bem = BaseErrorMeasure()

        for percentage in [-1.2, -0.1, 100.1, 123.9]:
            try:
                bem = BaseErrorMeasure(percentage)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

        for percentage in [0.0, 12.3, 53.4, 100.0]:
            try:
                bem = BaseErrorMeasure(percentage)
            except ValueError:    # pragma: no cover
                assert False      # pragma: no cover

    def get_error_initialization_test(self):
        """Test the get_error of BaseErrorMeasure for the initialization exception."""
        bem = BaseErrorMeasure()

        try:
            bem.get_error()
        except StandardError:
            pass
        else:
            assert False    # pragma: no cover

    def double_initialize_test(self):
        """Test for the error ocuring when the same error measure is initialized twice."""
        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg  = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)


        bem = BaseErrorMeasure()

        bem_calculate  = bem._calculate
        bem_local_error = bem.local_error
        
        def return_zero(ignoreMe, ignoreMeToo):
            return 0

        ## remove the NotImplementedErrors for initialization
        bem.local_error = return_zero
        bem._calculate   = return_zero
        
        ## correct initialize call
        bem.initialize(tsOrg, tsCalc)

        ## incorrect initialize call
        for cnt in xrange(10):
            try:
                bem.initialize(tsOrg, tsCalc)        
            except StandardError:
                pass
            else:
                assert False    # pragma: no cover

    def initialize_test(self):
        """Test if calculate throws an error as expected."""
        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg  = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        try:
            bem.initialize(tsOrg, tsCalc)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

        assert not bem.initialize(tsOrg, TimeSeries())

    def get_error_parameter_test(self):
        """Test for the parameter validity of get_error()."""
        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg  = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        bem_calculate  = bem._calculate
        bem_local_error = bem.local_error
        
        def return_zero(ignoreMe, ignoreMeToo):
            return 0

        ## remove the NotImplementedErrors for initialization
        bem.local_error = return_zero
        bem._calculate   = return_zero
        bem.initialize(tsOrg, tsCalc)

        bem.local_error = bem_local_error
        bem._calculate  = bem_calculate

        try:
            bem.get_error(10.0, 90.0)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

        for start in [-1.0, 80.0, 103.0]:
            for end in [-5.0, 10.0, 105.0]:
                try:
                    bem.get_error(start, end)
                except ValueError:
                    pass
                else:
                    assert False    # pragma: no cover

    def local_error_test(self):
        """Test local_error of BaseErrorMeasure."""
        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg  = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)

        bem = BaseErrorMeasure()

        for idx in xrange(len(tsOrg)):
            try:
                bem.local_error(tsOrg[idx][1], tsCalc[idx][1])
            except NotImplementedError:
                pass
            else:
                assert False    # pragma: no cover

class MeanSquaredErrorTest(unittest.TestCase):
    """Testing MeanSquaredError."""

    def local_error_test(self):
        """Test the local error of MeanSquaredError."""
        orgValues = [11, 33.1, 2.3, 6.54, 123.1, 12.54, 12.9]
        calValues = [24, 1.23, 342, 1.21, 4.112, 9.543, 3.54]

        mse = MeanSquaredError()
        for idx in xrange(len(orgValues)):
            res = (calValues[idx] - orgValues[idx])**2.0
            assert  str(res)[:6] == str(mse.local_error(orgValues[idx], calValues[idx]))[:6]

    def number_of_comparisons_test(self):
        """Test MeanSquaredError for a valid response to the minimalErrorCalculationPercentage."""
        dataOrg  = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9]]
        dataCalc = [[0,0],[1,1],[2,2],[3,3],[4,4],[5.1,5],[6.1,6],[7.1,7],[8.1,8],[9.1,9]]

        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        mse = MeanSquaredError(60.0)

        ## only 50% of the original TimeSeries have a corresponding partner
        if mse.initialize(tsOrg, tsCalc):
            assert False    # pragma: no cover

        if not mse.initialize(tsOrg, tsOrg):
            assert False    # pragma: no cover

    def error_calculation_test(self):
        """Test for a valid error calculation."""
        dataOrg         = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,  6], [7,7], [8,8],   [9,9]]
        dataCalc        = [[0,1], [1,3], [2,5], [3,0], [4,3], [5,5], [6.1,6], [7,3], [8.1,8], [9,8]]
        # difference:         1      2      3      3      1      0       NA      4       NA      1
        # local errors:       1      4      9      9      1      0       NA     16       NA      1

        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        mse = MeanSquaredError(80.0)
        mse.initialize(tsOrg, tsCalc)

        assert str(mse.get_error()) == "5.125"

class SymmetricMeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Testing symmetric mean absolute percentage error.

    Data extracted from http://monashforecasting.com/index.php?title=SMAPE#Example"""

    def local_error_test(self):
        """Test SymmetricMeanAbsolutePercentageError local error."""
        dataPtsOrg  = [2.30,     .373,           .583,          1.88,  1.44,         -0.0852, -.341,  .619,  .131,  1.27, 4.0]
        dataPtsCalc = [-1.21,   -.445,           .466,          .226, -.694,           -.575,  2.73, -1.49, -1.45, -.193, 4.0]
        localErrors = [  2.0,     2.0, 0.223069590086, 1.57075023742,   2.0,   1.48379279006,   2.0,   2.0,   2.0,   2.0, 0.0]

        smape = SymmetricMeanAbsolutePercentageError()

        for idx in xrange(len(dataPtsOrg)):
            le = smape.local_error(dataPtsOrg[idx], dataPtsCalc[idx])
            ple = localErrors[idx]

            ## compare the strings due to accuracy
            assert str(le) == str(ple)

    def error_calculation_test(self):
        """Test the calculation of the SymmetricMeanAbsolutePercentageError."""
        dataPtsOrg  = [2.30,     .373,           .583,          1.88,  1.44,         -0.0852, -.341,  .619,  .131,  1.27, 0]
        dataPtsCalc = [-1.21,   -.445,           .466,          .226, -.694,           -.575,  2.73, -1.49, -1.45, -.193, 0]

        tsOrg  = TimeSeries()
        tsCalc = TimeSeries()
        
        for idx in xrange(len(dataPtsOrg)):
            tsOrg.add_entry(float(idx),  dataPtsOrg[idx])
            tsCalc.add_entry(float(idx), dataPtsCalc[idx])

        smape = SymmetricMeanAbsolutePercentageError()
        smape.initialize(tsOrg, tsCalc)

        ## compare the strings due to accuracy
        assert "1.5706" == str(smape.get_error())[:6]

class MeanAbsoluteDeviationErrorTest(unittest.TestCase):
    """Testing symmetric mean absolute deviation error."""

    def local_error_test(self):
        """Test SymmetricMeanAbsolutePercentageError local error."""
        dataPtsOrg  = [ 2.30,  .373, .583, 1.880, 500]
        dataPtsCalc = [-1.21, -.445, .466,  .226, 300]
        localErrors = [ 3.51,  .818, .117, 1.654, 200]

        mad = MeanAbsoluteDeviationError()

        for idx in xrange(len(dataPtsOrg)):
            le = mad.local_error(dataPtsOrg[idx], dataPtsCalc[idx])
            ple = localErrors[idx]

            ## compare the strings due to accuracy
            #print le, ple
            assert str(le) == str(ple)

    def error_calculation_test(self):
        """Test the calculation of the SymmetricMeanAbsolutePercentageError."""
        dataPtsOrg  = [2.30,     .373,           .583,          1.88,  1.44,         -0.0852, -.341,  .619,  .131,  1.27, 0]
        dataPtsCalc = [-1.21,   -.445,           .466,          .226, -.694,           -.575,  2.73, -1.49, -1.45, -.193, 0]

        tsOrg  = TimeSeries()
        tsCalc = TimeSeries()
        
        for idx in xrange(len(dataPtsOrg)):
            tsOrg.add_entry(float(idx),  dataPtsOrg[idx])
            tsCalc.add_entry(float(idx), dataPtsCalc[idx])

        mad = MeanAbsoluteDeviationError()
        mad.initialize(tsOrg, tsCalc)

        ## compare the strings due to accuracy
        #print str(mad.get_error())[:6]
        assert "1.5406" == str(mad.get_error())[:6]

class MedianAbsolutePercentageErrorTest(unittest.TestCase):

    def error_calculation_test(self):
        """Test the MdAPE error calculation."""
        dataOrg         = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,8], [7.3, 5], [8, 0], [9,10]]
        dataCalc        = [[1,3], [2,5], [3,0], [4,3], [5,5], [6.1,6], [7,3], [7.3, 5], [8, 0], [9,9]]
                
        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)

        em = MedianAbsolutePercentageError()
        em.initialize(tsOrg, tsCalc)

        assert em.get_error() == 62.5
        assert em.get_error(20.0, 50.0) == 100.0

class MeanAbsoluteScaledErrorTest(unittest.TestCase):

    def initialization_error_test(self):
        """Test for the exceptions raised during initialization."""
        MeanAbsoluteScaledError(minimalErrorCalculationPercentage=60.0, historyLength=20.0)

        try:
            MeanAbsoluteScaledError(60.0, 0.0)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            MeanAbsoluteScaledError(60.0, -12.0)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            MeanAbsoluteScaledError(60.0, 120.0)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

        try:
            mase = MeanAbsoluteScaledError(60.0, 60.0)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover

    def calculate_historic_means_test(self):
        """Test the calculation of the historic means."""
        dataOrg = [[1.0, 10], [2.0, 12], [3.0, 14], [4.0, 13], [5.0, 17], [6.0, 20], [7.0, 23], [8.0, 26], [9.0, 29], [10.0, 31], [11.0, 26], [12.0, 21], [13.0, 18], [14.0, 14], [15.0, 13], [16.0, 19], [17.0, 24], [18.0, 28], [19.0, 30], [20.0, 32]]
        ##                           2          2          1          4          3          3          3          3           2           5           5           3           4           1           6           5           4           2           2
        ## Sum(History)                                                         12         13         14         16          14          16          18          18          19          18          19          19          20          18          19                                          
        correctResult = [                                                      2.4,       2.6,       2.8,       3.2,        2.8,        3.2,        3.6,        3.6,        3.8,        3.6,        3.8,        3.8,        4.0,        3.6]

        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        mase  = MeanAbsoluteScaledError(historyLength=5)
        result = mase._get_historic_means(tsOrg)
        
        assert result == correctResult

    def local_error_calculation_test(self):
        """Testing the mean absolute error calculation of the MASE."""
        dataOrg = [[1.0, 10], [2.0, 12], [3.0, 14], [4.0, 13], [5.0, 17], [6.0, 20], [7.0, 23], [8.0, 26], [9.0, 29], [10.0, 31], [11.0, 26], [12.0, 21], [13.0, 18], [14.0, 14], [15.0, 13], [16.0, 19], [17.0, 24], [18.0, 28], [19.0, 30], [20.0, 32]]
        dataFor = [[1.0, 11], [2.0, 13], [3.0, 14], [4.0, 11], [5.0, 13], [6.0, 18], [7.0, 20], [8.0, 26], [9.0, 21], [10.0, 34], [11.0, 23], [12.0, 23], [13.0, 15], [14.0, 12], [15.0, 14], [16.0, 17], [17.0, 25], [18.0, 22], [19.0, 14], [20.0, 30]]

        historyLength = 5
        em = MeanAbsoluteScaledError(historyLength=historyLength)

        ## A history length of 5 implies that the first 6 values have to be ignored for error calculation
        historyLength += 1
        dataOrg = dataOrg[historyLength:]
        dataFor = dataFor[historyLength:]

        for orgValue, forValue in zip(dataOrg, dataFor):
            difference = orgValue[1] - forValue[1]
            difference = abs(difference)

            assert difference == em.local_error(orgValue[1], forValue[1])

    def initialization_test(self):
        """Test for MASE initialization."""
        dataOrg = [[1.0, 10], [2.0, 12], [3.0, 14], [4.0, 13], [5.0, 17], [6.0, 20], [7.0, 23], [8.0, 26], [9.0, 29], [10.0, 31], [11.0, 26], [12.0, 21], [13.0, 18], [14.0, 14], [15.0, 13], [16.0, 19], [17.0, 24], [18.0, 28], [19.0, 30], [20.0, 32]]
        dataFor = [[1.0, 11], [2.0, 13], [3.0, 14], [4.0, 11], [5.0, 13], [6.0, 18], [7.0, 20], [8.0, 26], [9.0, 21], [10.0, 34], [11.0, 23], [12.0, 23], [13.0, 15], [14.0, 12], [15.0, 14], [16.0, 17], [17.0, 25], [18.0, 22], [19.0, 14], [20.0, 30]]
        
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsFor = TimeSeries.from_twodim_list(dataFor)

        em = MeanAbsoluteScaledError(historyLength=5)
        em.initialize(tsOrg, tsFor)

        assert len(em._errorValues) == len(em._historicMeans), "For each error value an historic mean has to exsist."

        try:
            em.initialize(tsOrg, tsFor)
        except StandardError:
            pass
        else:
            assert False    # pragma: no cover

        em = MeanAbsoluteScaledError(historyLength=20.0)
        em.initialize(tsOrg, tsFor)

        assert len(em._errorValues) == len(em._historicMeans), "For each error value an historic mean has to exsist."
        assert em._historyLength == 4, "The history is %s entries long. 4 were expected." % em._historyLength

        em = MeanAbsoluteScaledError(historyLength=40.0)
        em.initialize(tsOrg, tsFor)

        assert len(em._errorValues) == len(em._historicMeans), "For each error value an historic mean has to exsist."
        assert em._historyLength == 8, "The history is %s entries long. 8 were expected." % em._historyLength

    def error_calculation_test(self):
        """Testing for the correct MASE calculation.

        History length is 5 in this test.
        """
        dataOrg = [[1.0, 10], [2.0, 12], [3.0, 14], [4.0, 13], [5.0, 17], [6.0, 20], [7.0, 23], [8.0, 26], [9.0, 29], [10.0, 31], [11.0, 26], [12.0, 21], [13.0, 18], [14.0, 14], [15.0, 13], [16.0, 19], [17.0, 24], [18.0, 28], [19.0, 30], [20.0, 32]]
        dataFor = [[1.0, 11], [2.0, 13], [3.0, 14], [4.0, 11], [5.0, 13], [6.0, 18], [7.0, 20], [8.0, 26], [9.0, 21], [10.0, 34], [11.0, 23], [12.0, 23], [13.0, 15], [14.0, 12], [15.0, 14], [16.0, 17], [17.0, 25], [18.0, 22], [19.0, 14], [20.0, 30]]
        ##                           2          2          1          4          3          3          3          3           2           5           5           3           4           1           6           5           4           2           2
        ## Sum(History)                                                         12         13         14         16          14          16          18          18          19          18          19          19          20          18          19                                          
        ## Mean(History) ##         ##         ##         ##         ##        2.4        2.6        2.8        3.2         2.8         3.2         3.6         3.6         3.8         3.6         3.8         3.8         4.0         3.6         3.8
        ## AE                                                                               3          0          8           3           3           2           3           2           1           2           1           6          16           2       
        ## Sum(AE)                                                                          3          3         11          14          17          19          22          24          25          27          28          34          50          52
        ## MAE                                                                              3        1.5      3.666         3.5         3.4       3.166       3.142           3       2.777         2.7       2.545       2.833       3.571       3.714                                                                                  
        ## MASE (0% - 100%)                                                              1.25      0.625      1.527       1.458       1.416       1.319       1.309        1.25       1.157       1.125        1.06        1.18       1.602       1.547

        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsFor = TimeSeries.from_twodim_list(dataFor)

        em = MeanAbsoluteScaledError(historyLength=5)
        em.initialize(tsOrg, tsFor)

        ## check for error calculation depending on a specific endpoint
        correctResult = [1.25, 0.625, 1.527, 1.458, 1.416, 1.319, 1.309, 1.25, 1.157, 1.125, "1.060", "1.180", 1.602, 1.547]
        percentage = 100.0 / len(correctResult) + 0.2
        for errVal in xrange(14):
            endPercentage = percentage * (errVal + 1)
            
            ## set maximum percentage
            if endPercentage > 100.0:
                endPercentage = 100.0

            calcErr    = str(em.get_error(endPercentage=endPercentage))[:5]
            correctRes = str(correctResult[errVal])[:5]

            assert calcErr == correctRes