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

import pybindgen, sys

pycastC = pybindgen.Module("pycastC")

## create the submodules of pycast
pycastC_errors       = pycastC.add_cpp_namespace("errors")
pycastC_common       = pycastC.add_cpp_namespace("common")
pycastC_methods      = pycastC.add_cpp_namespace("methods")
pycastC_optimization = pycastC.add_cpp_namespace("optimization")

## pycast.errors
pycastC_errors.add_include('"pycast/errors/opt/baseerrormeasure.h"')
pycastC_errors_baseerrormeasure = pycastC_errors.add_cpp_namespace("baseerrormeasure")
pycastC_errors_baseerrormeasure_BaseErrorMeasure = pycastC_errors_baseerrormeasure.add_cpp_namespace("BaseErrorMeasure")

pycastC_errors_baseerrormeasure_BaseErrorMeasure.add_function(
    "initialize",
    # return value can't be bool because bool function cannot indicate exceptions by returning NULL (interpreted as False)
    pybindgen.retval("PyObject*", caller_owns_return=False), 
	[
	    pybindgen.param("PyObject*", "self",                  transfer_ownership=False),
		pybindgen.param("PyObject*", "originalTimeSeries",    transfer_ownership=False),
		pybindgen.param("PyObject*", "calculatedTimesSeries", transfer_ownership=False)
	])


## generate :)
pycastC.generate(sys.stdout)