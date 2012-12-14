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

from pycastobject import PyCastObject

def optimized(fn):
    def _optimized(self, *args, **kwargs):
        if self.optimization_enabled:
            class_name = self.__class__.__name__
            module = self.__module__.replace('pycast', 'pycastC')
            try:
                imported = __import__(module+"."+class_name, globals(), locals(), [fn.__name__])
                function = getattr(imported, fn.__name__)
                return function(self, *args, **kwargs)
            except ImportError:
                print "[WARNING] Could not enable optimization for %s, %s" % (fn.__name__, self)
                return fn(self, *args, **kwargs)
        else:
            return fn(self, *args, **kwargs)
    return _optimized