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
import json

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
