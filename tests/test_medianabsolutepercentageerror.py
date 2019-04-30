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
from pycast.errors.medianabsolutepercentageerror import MedianAbsolutePercentageError
from pycast.common.timeseries import TimeSeries


class TestMedianAbsolutePercentageError:
    """Tests the MedianAbsolutePercentageError for calculating the correct values."""

    def setup(self):
        """Sets up a test case."""
        self.original_data = [1.0,    2.3,    0.1,    -2.0,   -1.0,   0.0,    -0.2,   -0.3,   0.15,   -0.2,   0]
        self.calculated_data = [1.2,   2.0,    -0.3,   -1.5,   -1.5,   0.3,    0.0,    0.3,    -0.15,  0.3,   0]
        # localErrors:   20     13.04   400     25      50      NA      100     200     200     250     NA

    def test_error_calculation(self):
        """ Test error calculation for MedianAbsolutePercentageError"""
        error_measure = MedianAbsolutePercentageError()

        original_timeseries  = TimeSeries()
        calculated_timeseries = TimeSeries()

        for idx in range(len(self.original_data)):
            original_timeseries.add_entry(float(idx),  self.original_data[idx])
            calculated_timeseries.add_entry(float(idx), self.calculated_data[idx])

        error_measure.initialize(original_timeseries, calculated_timeseries)

        assert 100 == error_measure.get_error()
        assert 50 == error_measure.get_error(20.0, 50.0)
