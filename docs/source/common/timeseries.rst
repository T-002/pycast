.. index

pycast.common.timeseries
========================

Normalization Levels
--------------------
A TimeSeries instance can be normalized by different time granularity levels.
Valid values for normalization levels required by :py:meth:`pycast.common.TimeSeries.normalize` are stored in
:py:data:`pycast.common.timeseries.NormalizationLevels`.

Those levels include:
  
  - "second"
  - "minute"
  - "hour"
  - "day"  
  - "week"
  - "2week"
  - "4week"

Fusion Methods
--------------
Fusion methods that can be used to fusionate multiple data points within the same time bucket.
This might sort the list it is used on.
Valid values for fusion methods required by :py:meth:`pycast.common.TimeSeries.normalize` are stored in
:py:data:`pycast.common.timeseries.FusionMethods`.

Valid fusion methods are:

  - "sum": Sums up all valid values stored in the specific time bucket
  - "mean": Calculates the mean value within the time bucket
  - "median": Calculates the median of the given time bucket values.  In the case the number of entries within that bucket is even, the larger of the both values will be chosen as median.

Interpolation Methods
---------------------
Interpolation methods that can be used for interpolation missing time buckets.
Valid values for interpolation methods required by :py:meth:`pycast.common.TimeSeries.normalize` are stored in
:py:data:`pycast.common.timeseries.InterpolationMethods`.

Valid values for interpolation methods are:

  - "linear": Use linear interpolation to calculate the missing values

TimeSeries
==========
.. autoclass:: pycast.common.timeseries.TimeSeries