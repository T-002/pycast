import unittest, json

from pycast.common.timeseries import TimeSeries
from pycast.common.json_encoder import PycastEncoder

class PycastEncoderTest(unittest.TestCase):
	""" Test class containing all the tests for pycast.common.json_encoder.PycastEncoder"""

	def encode_timeseries_test(self):
		""" Test if a time series is converted into a string correctly"""

		data = [[1.5, 152.0],[2.5, 172.8],[3.5, 195.07200000000003],[4.5, 218.30528000000004]]
		ts = TimeSeries.from_twodim_list(data)
		data_json = json.dumps(ts, cls=PycastEncoder)
		#print data_json
		assert data_json == "[[1.5, 152.0], [2.5, 172.8], [3.5, 195.07200000000003], [4.5, 218.30528000000004]]"

	def encode_normal_object_test(self):
		"""Test if our encoder encodes regular python objects just like the default encoder"""
		obj = {1: 2}
		normal_encode = json.dumps(obj)
		our_encode = json.dumps(obj, cls=PycastEncoder)
		assert normal_encode == our_encode