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
from pycast.methods.exponentialsmoothing import ExponentialSmoothing

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
        try:
            self.execute()
            assert False
        except:
            assert True

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
        sm = ExponentialSmoothing(0.2, 7)
        
        try:
            sm = ExponentialSmoothing(-0.1, 7)
            assert False
        except ValueError:
            pass

        try:
            sm = ExponentialSmoothing(1.1, 7)
            assert False
        except ValueError:
            pass

        assert True



