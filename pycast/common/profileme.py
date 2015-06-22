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

try:
    import cProfile as profile
except ImportError:   # pragma: no cover
    import profile    # pragma: no cover

class _ProfileDecorator(object):

    """Decorator class that build a wrapper around any function.

    :warning: The decorator does not take recursive calls into account!
    """

    def __init__(self, filelocation):
        """Initializes the ProfileMe decorator.

        :param function func:    Function that will be profiles.
        :param string filelocation:    Location for the profiling results.
        """
        super(_ProfileDecorator, self).__init__()
        self._filelocation = filelocation

    def __call__(self, func):
        """Returns a wrapped version of the called function.

        :param function func:    Function that should be wrapped.

        :return:    Returns a wrapped version of the called function.
        :rtype:     function
        """
        def wrapped_func(*args, **kwargs):
            """This function gets executed, if the wrapped function gets called.

            It automatically created a performance profile for the corresponding function call.
            """
            # create the profiler and execute the called function
            profiler = profile.Profile()
            result   = profiler.runcall(func, *args, **kwargs)

            # store the performance profile
            filename = "%s" % (self._filelocation)
            profiler.dump_stats(filename)

            # return the result
            return result

        self._func = func
        setattr(wrapped_func, "__name__", self._func.__name__)
        setattr(wrapped_func, "__repr__", self._func.__repr__)
        setattr(wrapped_func, "__str__", self._func.__str__)
        setattr(wrapped_func, "__doc__", self._func.__doc__)

        return wrapped_func

# This is the "real decorator"
# Usage: @profileMe
profileMe = _ProfileDecorator
