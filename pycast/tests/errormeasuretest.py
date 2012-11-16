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

        bem_calculate  = bem.calculate
        bem_local_error = bem.local_error
        
        def return_zero(ignoreMe, ignoreMeToo):
            return 0

        ## remove the NotImplementedErrors for initialization
        bem.local_error = return_zero
        bem.calculate   = return_zero
        bem.initialize(tsOrg, tsCalc)

        bem.local_error = bem_local_error
        bem.calculate  = bem_calculate

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
            res = (calValues[idx] - orgValues[idx])**2
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
        print mse.get_error()

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

        print "Calculated Error: %s" % smape.get_error()

        ## compare the strings due to accuracy
        assert "1.5706" == str(smape.get_error())[:6]
