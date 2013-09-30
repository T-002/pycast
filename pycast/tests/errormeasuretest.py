#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#Copyright (c) 2012-2013 Christian Schwarz
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
from pycast.common.timeseries import TimeSeries
from pycast.common.pycastobject import PyCastObject

class BaseErrorMeasureTest(unittest.TestCase):
    """Test class for the BaseErrorMeasure interface."""

    def initialization_test(self):
        """Test the BaseErrorMeasure initialization."""
        BaseErrorMeasure()

        for percentage in [-1.2, -0.1, 100.1, 123.9]:
            try:
                BaseErrorMeasure(percentage)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

        for percentage in [0.0, 12.3, 53.4, 100.0]:
            try:
                BaseErrorMeasure(percentage)
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

        bem.local_error = bem_calculate
        bem._calculate   = bem_local_error

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
        
        def return_zero(ignoreMe, ignoreMeToo, andMe=None, andMeToo=None):
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
                bem.local_error([tsOrg[idx][1]], [tsCalc[idx][1]])
            except NotImplementedError:
                pass
            else:
                assert False    # pragma: no cover

    def optimized_test(self):
        """Check if all tests are passed, using optimized implementations."""
        PyCastObject.enable_global_optimization()
        self.get_error_initialization_test()
        self.initialization_test()
        self.initialize_test()
        self.double_initialize_test()
        PyCastObject.disable_global_optimization()


















