.. index

Performance Optimization
========================
Based on the complexity of smoothing and forecasting algorithms, pycast implements performance critical methods in C++ or OpenCL.
To enable those optimized functions, you need to execute the following::

    import pycast.common.PyCastObject
    PyCastObject.enable_global_optimization()

To disable the optimized functions::

    import pycast.common.PyCastObject
    PyCastObject.disable_global_optimization()

All objects instantiated after one of those calls will use / not use the optimized functions. All existing instances will not be changed.

Code Example
------------

Based on existing C++ Functions, you can enable optimization for your instances.
Therefore you need to:

  * inherit from pycast.common.PyCastObject
  * implement :py:meth:`_build_optimization_dictionary(self)`

An example implementation looks like the following::

    from pycast.common import PyCastObject
    class CustomObject(PyCastObject):
        """Your custom class."""

        def _build_optimization_dictionary(self):
        """Creates a dictionary that maps optimized to not optimized methods."""
        super(CustomObject, self)._build_optimization_dictionary()

        try:
            from pycastC.<submodule>.CustomObject import optimized_method
        except ImportError:                                                                      # pragma: no cover
            print "[WARNING] Could not enable optimization for %s." % self.__class__.__name__    # pragma: no cover
            pass                                                                                 # pragma: no cover
        else:
            self._methodOptimizationDictionary["methodname"] = [CustomObject.method, optimized_method]

        def method(self):
            """This is the python implementation of the method that should be replaced with an optimized version."""

