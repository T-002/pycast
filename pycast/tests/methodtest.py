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
import unittest, os, random

## required modules from pycast
from pycast.common.timeseries import TimeSeries
from pycast.methods.basemethod import BaseMethod
from pycast.methods.simplemovingaverage import SimpleMovingAverage
from pycast.methods.exponentialsmoothing import ExponentialSmoothing, HoltMethod, HoltWintersMethod

class BaseMethodTest(unittest.TestCase):
    """Test class containing all tests for pycast.method.basemethod."""

    def initialization_test(self):
        """Test BaseMethod initialization."""
        hasToBeSorted     = random.choice([True, False])
        hasToBeNormalized = random.choice([True, False])
        b = BaseMethod(["param1", "param2"], hasToBeSorted=hasToBeSorted, hasToBeNormalized=hasToBeNormalized)

        if not b.has_to_be_sorted()     == hasToBeSorted:     raise AssertionError
        if not b.has_to_be_normalized() == hasToBeNormalized: raise AssertionError

    def parameter_set_test(self):
        """Test if the parameters of a method are set correctly."""
        b = BaseMethod(["param1", "param2"])
        b.add_parameter("param1", 1)
        b.add_parameter("param2", 2)
        b.add_parameter("param1", 1)

        if not len(b._parameters) == 2: raise AssertionError

    def method_completition_Test(self):
        """Test if methods detect their executable state correctly."""
        b = BaseMethod(["param1", "param2"])

        if b.can_be_executed(): raise AssertionError
        
        b.add_parameter("param1", 1)
        if b.can_be_executed(): raise AssertionError

        b.add_parameter("param2", 2)
        if not b.can_be_executed(): raise AssertionError

    def execute_not_implemented_exception_test(self):
        """Test the correct interface of BaseMethod."""
        b = BaseMethod(["param1", "param2"])

        data  = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        ts = TimeSeries.from_twodim_list(data)
        ts.normalize("second")

        try:
            b.execute(ts)
        except NotImplementedError:
            pass
        else:
            assert False    # pragma: no cover

class SimpleMovingAverageTest(unittest.TestCase):
    """Test class for the SimpleMovingAverage method."""

    def initialization_test(self):
        """Test the initialization of the SimpleMovingAverage method."""
        sm = SimpleMovingAverage(3)
        
        if not sm._parameters["windowsize"] == 3:   raise AssertionError

    def execute_test(self):
        """Test the execution of SimpleMovingAverage."""
        ## Initialize the source
        data  = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")


        ## Initialize a correct result.
        ### The numbers look a little bit odd, based on the binary translation problem
        data  = [[1.5, 0.10000000000000002],[2.5, 0.20000000000000004],[3.5, 0.3]]
        tsDst = TimeSeries.from_twodim_list(data)

        ## Initialize the method
        sma = SimpleMovingAverage(3)
        res = tsSrc.apply(sma)

        if not res == tsDst: raise AssertionError

class ExponentialSmoothingTest(unittest.TestCase):
    """Test class for the ExponentialSmoothing method."""
    
    def initialization_test(self):
        """Test the initialization of the ExponentialSmoothing method."""
        sm = ExponentialSmoothing(0.2, 0)
        
        for alpha in [-0.1, 1.1, 3.1, -4.2]:
            try:
                ExponentialSmoothing(alpha)
            except ValueError:
                pass
            else:
                assert False    # pragma: no cover

    def smoothing_test(self):
        """Test smoothing part of ExponentialSmoothing."""
        data  = [[0, 10.0], [1, 18.0], [2, 29.0], [3, 15.0], [4, 30.0], [5, 30.0], [6, 12.0], [7, 16.0]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")

        ## Initialize a correct result.
        ### The numbers look a little bit odd, based on the binary translation problem
        data  = [[1.5, 10.0],[2.5, 12.4],[3.5, 17.380000000000003],[4.5, 16.666],[5.5, 20.6662],[6.5, 23.46634],[7.5, 20.026438],[8.5, 18.8185066]]
        tsDst = TimeSeries.from_twodim_list(data)

        ## Initialize the method
        es = ExponentialSmoothing(0.3, 1)
        res = tsSrc.apply(es)

        if not res == tsDst: raise AssertionError

    def forecasting_test(self):
        """Test forecast part of ExponentialSmoothing."""
        data  = [[0, 10.0], [1, 18.0], [2, 29.0], [3, 15.0], [4, 30.0], [5, 30.0], [6, 12.0], [7, 16.0]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")
        
        es = ExponentialSmoothing(0.1, 7)
        res = tsSrc.apply(es)

        ## test if the correct number of values have been forecasted
        assert len(tsSrc)  + 6 == len(res)

class HoltMethodTest(unittest.TestCase):
    """Test class for the HoltMethod method."""
    
    def initialization_test(self):
        """Test the initialization of the HoltMethod method."""
        HoltMethod(0.2, 0.3)
        
        for alpha in [-0.1, 1.1]:
            for beta in [-1.4, 3.2]:
                try:
                    HoltMethod(alpha, beta)
                except ValueError:
                    pass
                else:
                    assert False    # pragma: no cover

    def smoothing_test(self):
        """Test smoothing part of ExponentialSmoothing."""
        data  = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")

        ## Initialize a correct result.
        ### The numbers look a little bit odd, based on the binary translation problem
        data  = [[1.5, 0.0],[2.5, 0.10000000000000002],[3.5, 0.12000000000000001],[4.5, 0.204]]
        tsDst = TimeSeries.from_twodim_list(data)

        ## Initialize the method
        hm = HoltMethod(0.2, 0.3, valuesToForecast=0)
        res = tsSrc.apply(hm)

        if not res == tsDst: raise AssertionError

    def forecasting_test(self):
        """Test forecast part of ExponentialSmoothing."""
        data  = [[0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsSrc = TimeSeries.from_twodim_list(data)
        tsSrc.normalize("second")
        
        hm = HoltMethod(0.2, 0.3, 5)
        res = tsSrc.apply(hm)

        ## test if the correct number of values have been forecasted
        assert len(tsSrc) + 4 == len(res)

class HoltWintersMethodTest(unittest.TestCase):
    """Test class for the HoltWintersMethod method."""
    
    def initialization_test(self):
        """Test the initialization of the HoltWintersMethod method."""
        HoltWintersMethod(0.2, 0.3, 0.4)
        
        for alpha in [-0.1, 1.1]:
            for beta in [-1.4, 3.2]:
                for gamma in [-0.05, 1.3]:
                    try:
                        HoltWintersMethod(alpha, beta, gamma)
                    except ValueError:
                        pass
                    else:
                        assert False    # pragma: no cover