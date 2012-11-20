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

## This module contains helper functions that will be moved later

import time

## @todo define a more general interface!
def linear_interpolation(first, last, steps):
    """Interpolates all missing values using linear interpolation.

    :param Numeric first:    Start value for the interpolation.
    :param Numeric last:    End Value for the interpolation
    :param Integer steps:    Number of missing values that have to be calculated.

    :return:    Returns a list of floats containing only the missing values.
    :rtype:     List
    """
    result = []

    for step in xrange(0, steps):
        fpart = (steps - step) * first
        lpart = (step + 1)            * last
        value = (fpart + lpart) / float(steps + 1)
        result.append(value)

    return result
