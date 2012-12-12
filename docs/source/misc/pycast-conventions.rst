.. index

pycast conventions
==================
pycast uses several conventions to make your live easier. While Python does not enforce those, you are strongly recommendet to follow our guidelines ;).

Naming Conventions
------------------
When using pycast variables, objects, methods and functions, the following naming conventions should help you to find what you are looking for. If you are developing functionality to be used within pycast, you should follow those guidelines as well.
  - variables, functions, methods, classes and modules starting with an underscore (_) should be seen as private, inheritable attributes of any entity
  - functions and methods use underscores (_) to delimit words while variables and classes use CamelCase

Documentation Conventions
-------------------------
pycast variables, objects, methods and functions are documented using Sphinx. When writting documentation, the following docstring can be used as starting point.

.. code-block:: html
    :linenos:

    """Some short info here.

    Some more detailed info here. If you need to write a list, use the following:

        - List item One
        - List item Two

    :param Type parameterNameFromSignature:    This is the documentation for the first
        parameter. It has some additional Type information if a specific Type is expected.
        Default data types are: Integer, Float, Numeric, String, List, Dictionary, Tuple,
        ClassNames, ...
    :param Type secondParameterNameFromSignature:    This is the documentation for
        the second parameter. Do not use an empty line between your parameters!

    :return:    If the function has a valid return value (other than :py:const:`None`),
        this should be used, including the following:
    :rtype:     The return type.

    :raise:    A short message, when a specific :py:exc:`Exception` is raised.

    :warning:    A warning if anything can be potentialy dangerous.

    :note:    An internal explanation for implementation details if not mentioned earlier.
    :todo:    A reminder for internal development discussions.
    """