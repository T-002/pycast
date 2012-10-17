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

from smoothingmethod import SmoothingMethod

class SimpleMovingAverage(SmoothingMethod):
    """Implements the simple moving average.
    
    The SMA algorithm will calculate the average value at time t based on the
    datapoints between [t - floor(windowsize / 2), t + floor(windowsize / 2)].
    
    Explanation: http://en.wikipedia.org/wiki/Moving_average
    """
    
    def __init__(self, windowsize=5):
        """Initializes the SimpleMovingAverage.
        
        @param windowsize Size of the SimpleMovingAverages window.
                          This number has to be uneven and positive.
        """
        super(SimpleMovingAverage, self).__init__(["windowsize"], True, True)
        self.add_parameter("windowsize", windowsize)
    
    