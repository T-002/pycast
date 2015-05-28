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


## required external modules
import unittest

## required modules from pycast
from pycast.errors import MeanAbsoluteScaledError
from pycast.common.timeseries import TimeSeries


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
            MeanAbsoluteScaledError(60.0, 60.0)
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

            assert difference == em.local_error([orgValue[1]], [forValue[1]])

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
        ## AD                                                                               3          0          8           3           3           2           3           2           1           2           1           6          16           2       
        ## Sum(AD)                                                                          3          3         11          14          17          19          22          24          25          27          28          34          50          52
        ## MAD                                                                              3        1.5      3.666         3.5         3.4       3.166       3.142           3       2.777         2.7       2.545       2.833       3.571       3.714                                                                                  
        ## MASE (0% - 100%)                                                              1.25      0.625      1.527       1.458       1.416       1.319       1.309        1.25       1.157       1.125        1.06        1.18       1.602       1.547

        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsFor = TimeSeries.from_twodim_list(dataFor)

        historyLength = 5
        em = MeanAbsoluteScaledError(historyLength=historyLength)
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

        for errVal in xrange(14):
            endDate = dataOrg[errVal + 6][0]
            
            calcErr    = str(em.get_error(endDate=endDate))[:5]
            correctRes = str(correctResult[errVal])[:5]
        
            assert calcErr == correctRes, "%s != %s" % (calcErr, correctRes)

        em.get_error(startDate=7.0)

        try:
            em.get_error(startDate=42.23)
        except ValueError:
            pass
        else:
            assert False    # pragma: no cover
