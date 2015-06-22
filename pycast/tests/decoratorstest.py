# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# Copyright (c) 2012-2015 Christian Schwarz
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

import unittest
from mock import Mock

from pycast.common.decorators import optimized
from pycast.common.timeseries import TimeSeries
from pycast.errors.baseerrormeasure import BaseErrorMeasure
import pycastC.errors.baseerrormeasure.BaseErrorMeasure as cerror

class OptimizedDecoratorTest(unittest.TestCase):

    def test_optimization_enabled(self):
        error = BaseErrorMeasure()
        error._enable_instance_optimization()

        cerror.initialize = Mock()

        error.initialize(None, None) #parameters irrelevant for this test
        assert cerror.initialize.called, "If optimization is enabled the c method should be called"

    def test_optimization_disabled(self):
        error = BaseErrorMeasure()
        error._disable_instance_optimization()

        cerror.initialize = Mock()

        try:
            error.initialize(None, None) #parameters irrelevant for this test
        except:
            pass
        assert not cerror.initialize.called, "If optimization is disabled the c method should not be called"

    def test_function_call_is_transparent(self):
        """
        With and without optimization the method
        should be called with the same parameters.
        """
        oldError = BaseErrorMeasure.local_error
        BaseErrorMeasure.local_error = Mock()
        ts = TimeSeries.from_twodim_list([[1,1]])

        error = BaseErrorMeasure()
        error._enable_instance_optimization()
        error.initialize(ts, ts)

        error = BaseErrorMeasure()
        error._disable_instance_optimization()
        error.initialize(ts, ts)
        BaseErrorMeasure.local_error = oldError

    def test_import_fail(self):
        """
        If the import of the cmodules
        fails the original method should be used
        """
        class Foo:
            def __init__(self):
                self.optimizationEnabled = True
                self.called = False
            @optimized
            def foo(self):
                self.called = True

        test_obj = Foo()
        test_obj.foo()
        assert test_obj.called, "If no cmodule exists, original method should be called"
