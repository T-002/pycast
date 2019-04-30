# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# Copyright (c) 2012-2019 Christian Schwarz
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

# required modules from pycast
from pycast.errors.meansquarederror import MeanSquaredError
from pycast.common.timeseries import TimeSeries


class TestMeanSquaredErrorTest:
    """Testing the MeanSquaredError."""

    def setup(self):
        """Sets up a test case."""
        self.original_data = [1.0, 2.3, 0.1, -2.0, -1.0, 0.0, -0.2, -0.3, 0.15, -0.2, 0]
        self.calculated_data = [1.2, 2.0, -0.3, -1.5, -1.5, 0.3, 0.0, 0.3, -0.15, 0.3, 0]

    def test_local_error(self):
        """Test MeanSquaredError.local_error."""
        error_measure = MeanSquaredError()

        for idx in range(len(self.original_data)):
            calc_local_error = error_measure.local_error([self.original_data[idx]], [self.calculated_data[idx]])
            expected_error = (self.calculated_data[idx] - self.original_data[idx]) ** 2
            assert expected_error == calc_local_error

    def test_error_calculation(self):
        """Test the calculation of the MeanSquaredError."""
        original_timeseries  = TimeSeries()
        calculated_timeseries = TimeSeries()

        for idx in range(len(self.original_data)):
            original_timeseries.add_entry(float(idx),  self.original_data[idx])
            calculated_timeseries.add_entry(float(idx), self.calculated_data[idx])

        error_measure = MeanSquaredError()
        error_measure.initialize(original_timeseries, calculated_timeseries)

        assert 0.14727272727272725 == error_measure.get_error()

#    def number_of_comparisons_test(self):
#        """Test MeanSquaredError for a valid response to the minimalErrorCalculationPercentage."""
#        dataOrg  = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9]]
#        dataCalc = [[0,0],[1,1],[2,2],[3,3],[4,4],[5.1,5],[6.1,6],[7.1,7],[8.1,8],[9.1,9]]
#
#        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
#        tsCalc = TimeSeries.from_twodim_list(dataCalc)
#
#        mse = MeanSquaredError(60.0)
#
#        # only 50% of the original TimeSeries have a corresponding partner
#        if mse.initialize(tsOrg, tsCalc):
#            assert False    # pragma: no cover
#
#        if not mse.initialize(tsOrg, tsOrg):
#            assert False    # pragma: no cover
#
#    def error_calculation_test(self):
#        """Test for a valid error calculation."""
#        dataOrg         = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,  6], [7,7], [8,8],   [9,9]]
#        dataCalc        = [[0,1], [1,3], [2,5], [3,0], [4,3], [5,5], [6.1,6], [7,3], [8.1,8], [9,8]]
#        # difference:         1      2      3      3      1      0       NA      4       NA      1
#        # local errors:       1      4      9      9      1      0       NA     16       NA      1
#
#        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
#        tsCalc = TimeSeries.from_twodim_list(dataCalc)
#
#        tsOrg  = TimeSeries.from_twodim_list(dataOrg)
#        tsCalc = TimeSeries.from_twodim_list(dataCalc)
#
#        mse = MeanSquaredError(80.0)
#        mse.initialize(tsOrg, tsCalc)
#
#        assert str(mse.get_error()) == "5.125"
#
#    def start_and_enddate_test(self):
#        """Testing for startDate, endDate exceptions."""
#        data   = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
#        tsOrg  = TimeSeries.from_twodim_list(data)
#        tsCalc = TimeSeries.from_twodim_list(data)
#
#        bem = MeanSquaredError()
#        bem.initialize(tsOrg, tsCalc)
#
#        for startDate in [0.0, 1, 2, 3]:
#            bem.get_error(startDate=startDate, endDate=4)
#
#        for endDate in [1, 2, 3, 4]:
#            bem.get_error(startDate=0.0, endDate=endDate)
#
#        try:
#            bem.get_error(startDate=23)
#        except ValueError:
#            pass
#        else:
#            assert False    # pragma: no cover
#
#        try:
#            bem.get_error(endDate=-1)
#        except ValueError:
#            pass
#        else:
#            assert False    # pragma: no cover
#
