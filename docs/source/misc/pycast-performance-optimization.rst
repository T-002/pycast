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

  * inherit from `pycast.common.PyCastObject`
  * decorate the original method with the 'optimized' decorator

An example implementation looks like the following::

    from pycast.common import PyCastObject
    from pycast.common.decorators import optimized
    class CustomObject(PyCastObject):
        """Your custom class."""

        @optimized
        def method(self):
            """This is the python implementation of the method that should be replaced with an optimized version."""

