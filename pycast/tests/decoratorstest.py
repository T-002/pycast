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
		error._disable_instance_optimization

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
		error = BaseErrorMeasure()
		error.local_error = Mock()
		ts = TimeSeries.from_twodim_list([[1,1]])

		error._enable_instance_optimization()
		error.initialize(ts, ts)

		error._disable_instance_optimization()
		error.initialize(ts, ts)

	def test_import_fail(self):
		"""
		If the import of the cmodules 
		fails the original method should be used
		"""
		class Foo:
			def __init__(self):
				self.optimization_enabled = True
				self.called = False
			@optimized
			def foo(self):
				self.called = True

		test_obj = Foo()
		test_obj.foo()
		assert test_obj.called, "If no cmodule exists, original method should be called"
