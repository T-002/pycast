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

class PyCastObject(object):
    """The base class for all pycast objects.

    This class is used to introduce a common interface for potential
    C/C++/OpenCL optimization within pycast, as well as other common
    tasks.
    """

    ## stores, if pycast should only create optimized instances.
    ### default = False
    _globalOptimize = False

    def __init__(self):
        """Initializes the PyCastObject."""
        super(PyCastObject, self).__init__()

        self._build_optimization_dictionary()

        if PyCastObject._globalOptimize:
            self._enable_instance_optimization()

    def _build_optimization_dictionary(self):
        """Creates a dictionary that maps optimized to not optimized methods."""
        self._methodOptimizationDictionary = {}

        ## example code
        #try:
        #    from pycastC.errors.BaseErrorMeasure import initialize
        #except ImportError:
        #    pass
        #else:
        #    self._methodOptimizationDictionary["initialize"] = [BaseErrorMeasure.initialize, initialize]


    def _enable_instance_optimization(self):
        """Enables the optimization for the PyCastObject instance.

        Within this method, python methods can be replaces with C++
        functions.

        :warning:    Do not forget to implement the disable_instance_optimization()
            as well.
        """
        for methodname in self._methodOptimizationDictionary:
            setattr(self, methodname, self._methodOptimizationDictionary[methodname][1])

    def _disable_instance_optimization(self):
        """Disables the optimization for the PyCastObject instance.

        Within this method, optimized C++ functions will be replaced by 
        the original python implementations.
        """
        setattr(self, methodname, self._methodOptimizationDictionary[methodname][0])

    @classmethod
    def enable_global_optimization(cls):
        """Enables the global optimization of pycast methods, if possible.

        By default, optimization is turned off.

        :note:    Only new created instances will be affected.
        """
        cls._globalOptimize = True

    @classmethod
    def disable_global_optimization(cls):
        """Disables the global optimization of pycast methods.

        :note:    Only new created instances will be affected.
        """
        cls._globalOptimize = False