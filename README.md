======
pycast
======

pycast aims to provide a python module supporting the basics as 
well as advanced smoothing and forecasting methods that can be used
on timeseries data.

Typical usage often looks like this:

    #!/usr/bin/env python
    
    from pycast.common.timeseries           import TimeSeries
    from pycast.methods.simplemovingaverage import SimpleMovingAverage
    
    ts = TimeSeries()
    ts.add_entry(0.0, 0.0)
    ts.add_entry(1.0, 0.8)
    ts.add_entry(2.1, 0.9)
    ts.add_entry(3.2, 1.3)
    ts.add_entry(4.0, 2.0)
    
    ts.normalize("second")
    smoothedTS = ts.apply(SimpleMovingAverage(3))
    

Some usage examples of pycast in combination with other tools like gnuplot
can be found in ``bin/examples``

Basic pycast objects
====================

pycast.common.timeseries.TimeSeries
------------------------------------
An instance of TimeSeries is used to store and use your timeseries data

TimeSeries instances:

* Store data
* Can be used to sort and normalize your timeseries data to predefined levels.

Currently, there are some restrictions:

1. TimeSeries can only contain single dimensional, floating point timeseries
2. For internal representation, the UNIX epochs are used

License
=======
Copyright (c) 2012 Christian Schwarz

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Contributors
============
Christian Schwarz

References
==========
* `Project site: https://github.com/T-002/pycast`.