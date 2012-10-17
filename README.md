======
pycast
======

pycast aims to provide a python module supporting the basics as 
well as advanced smoothing and forecasting methods that can be used
on timeseries data.

Typical usage often looks like this::

    #!/usr/bin/env python
    
    from pycast.common.timeseries import TimeSeries
    # more code will follow here

Some usage examples of pycast in combination with other tools like gnuplot
can be found in ``bin/examples``

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.

Basic pycast objects
====================

pycast.commonf.timeseries.TimeSeries
------------------------------------
An instance of TimeSeries is used to store and use your timeseries data

TimeSeries instances:

* Store data
* Can be used to sort and normalize your timeseries data to predefined levels.

Currently, there are some restrictions:

1. TimeSeries can only contain single dimensional, floating point timeseries
2. For internal representation, the UNIX epochs are used

Contributors
============
Christian Schwarz

References
==========
* `Project site: http://code.google.com/p/py-cast/`_.