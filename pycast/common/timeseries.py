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

"""Module contains all components corresponding to TimeSeries data."""

import time
import random
import os

## some string constants
_STR_EPOCHS = "UNIX-epochs"

os.environ['TZ'] = 'GMT'

## Time series levels that can be used for normalization.
NormalizationLevels = {
    "second":  1,
    "minute":  1 * 60,
    "hour":    1 * 60 * 60,
    "day":     1 * 60 * 60 * 24,
    "week":    1 * 60 * 60 * 24 * 7,
    "2week":   1 * 60 * 60 * 24 * 7 * 2,
    "4week":   1 * 60 * 60 * 24 * 7 * 4
}

## Fusion methods that can be used to fusionate multiple data points within
## the same time bucket. This might sort the list it is used on.
FusionMethods = {
    "mean":       lambda l: sum(l) / float(len(l)),    # pragma: no cover
    "median":     lambda l: sorted(l)[len(l)//2],      # pragma: no cover
    "sum":        lambda l: sum(l)                     # pragma: no cover
}

## Interpolation methods that can be used for interpolation missing data points.
from helper import linear_interpolation
InterpolationMethods = {
    "linear": linear_interpolation
}

from pycastobject import PyCastObject
class TimeSeries(PyCastObject):
    """A TimeSeries instance stores all relevant data for a real world time series.

    :warning: TimeSeries instances are NOT thread-safe.
    """

    def __init__(self, isNormalized=False, isSorted=False):
        """Initializes the TimeSeries.

        :param boolean isNormalized:    Within a normalized TimeSeries, all data points
            have the same temporal distance to each other.
            When this is :py:const:`True`, the memory consumption of the TimeSeries might be reduced.
            Also algorithms will probably run faster on normalized TimeSeries.
            This should only be set to :py:const:`True`, if the TimeSeries is really normalized!
            TimeSeries normalization can be forced by executing :py:meth:`TimeSeries.normalize`.
        :param boolean isSorted:    If all data points added to the time series are added
            in their ascending temporal order, this should set to :py:const:`True`.
        """
        super(TimeSeries, self).__init__()
        self._normalized           = True
        self._normalizationLevel   = None
        self._predefinedNormalized = isNormalized

        self._sorted               = isSorted
        self._predefinedSorted     = isSorted

        self._timeseriesData = []

        self._timestampFormat = None

    def set_timeformat(self, tsformat=None):
        """Sets the TimeSeries global time format.

        :param string tsformat:    Format of the timestamp. This is used to convert the
            timestamp from UNIX epochs when the TimeSeries gets serialized by :py:meth:`TimeSeries.to_json` and
            :py:meth:`TimeSeries.to_gnuplot_datafile`. For valid examples take a look into the :py:func:`time.strptime`
            documentation.
        """
        self._timestampFormat = tsformat

    def to_gnuplot_datafile(self, datafilepath):
        """Dumps the TimeSeries into a gnuplot compatible data file.

        :param string datafilepath:    Path used to create the file. If that file already exists,
            it will be overwritten!

        :return:   Returns :py:const:`True` if the data could be written, :py:const:`False` otherwise.
        :rtype:    boolean
        """
        try:
            datafile = file(datafilepath, "wb")
        except Exception:
            return False

        if self._timestampFormat is None:
            self._timestampFormat = _STR_EPOCHS

        datafile.write("## time_as_<%s> value\n" % self._timestampFormat)

        convert = TimeSeries.convert_epoch_to_timestamp
        for datapoint in self._timeseriesData:
            timestamp, value = datapoint
            if self._timestampFormat is not None:
                timestamp = convert(timestamp, self._timestampFormat)

            datafile.write("%s %s\n" % (timestamp, value))

        datafile.close()
        return True

    def __copy__(self):
        """Returns a new clone of the TimeSeries.

        :return:    Returns a TimeSeries containing the same data and configuration as self.
        :rtype:     TimeSeries
        """
        ts = TimeSeries.from_twodim_list(self._timeseriesData)

        ts._normalizationLevel   = self._normalizationLevel
        ts._normalized           = self._normalized
        ts._sorted               = self._sorted
        ts._predefinedSorted     = self._predefinedSorted
        ts._predefinedNormalized = self._predefinedNormalized
        ts._timestampFormat      = self._timestampFormat

        return ts

    def to_twodim_list(self):
        """Serializes the TimeSeries data into a two dimensional list of [timestamp, value] pairs.

        :return:    Returns a two dimensional list containing [timestamp, value] pairs.
        :rtype:     list
        """
        tsformat = self._timestampFormat

        if tsformat is None:
            return self._timeseriesData

        datalist = []
        append   = datalist.append
        convert  = TimeSeries.convert_epoch_to_timestamp
        for entry in self._timeseriesData:
            append([convert(entry[0], tsformat), entry[1]])

        return datalist

    @classmethod
    def from_twodim_list(cls, datalist, tsformat=None):
        """Creates a new TimeSeries instance from the data stored inside a two dimensional list.

        :param list datalist:    List containing multiple iterables with at least two values.
            The first item will always be used as timestamp in the predefined format,
            the second represents the value. All other items in those sublists will be ignored.
        :param string tsformat:    Format of the given timestamp. This is used to convert the
            timestamp into UNIX epochs, if necessary. For valid examples take a look into
            the :py:func:`time.strptime` documentation.

        :return:    Returns a TimeSeries instance containing the data from datalist.
        :rtype:     TimeSeries
        """
        ## create and fill the given TimeSeries
        ts = TimeSeries()
        ts.set_timeformat(tsformat)

        for entry in datalist:
            ts.add_entry(*entry[:2])

        ## set the normalization level
        ts._normalized = ts.is_normalized()
        ts.sort_timeseries()

        return ts

    def initialize_from_sql_cursor(self, sqlcursor):
        """Initializes the TimeSeries's data from the given SQL cursor.

        You need to set the time stamp format using :py:meth:`TimeSeries.set_timeformat`.

        :param SQLCursor sqlcursor:    Cursor that was holds the SQL result for any given
            "SELECT timestamp, value, ... FROM ..." SQL query.
            Only the first two attributes of the SQL result will be used.

        :return:    Returns the number of entries added to the TimeSeries.
        :rtype:     integer
        """
        ## initialize the result
        tuples = 0

        ## add the SQL result to the time series
        data = sqlcursor.fetchmany()
        while 0 < len(data):
            for entry in data:
                self.add_entry(str(entry[0]), entry[1])

            data = sqlcursor.fetchmany()

        ## set the normalization level
        self._normalized = self._check_normalization

        ## return the number of tuples added to the timeseries.
        return tuples

    def __str__(self):
        """Returns a string representation of the TimeSeries.

        :return:    Returns a string representing the TimeSeries in the format:

            "TimeSeries([timestamp, data], [timestamp, data], [timestamp, data])".
        :rtype:     string
        """
        return """TimeSeries(%s)""" % ",".join([str(entry) for entry in self._timeseriesData])

    def __add__(self, otherTimeSeries):
        """Creates a new TimeSeries instance containing the data of :py:obj:`self` and otherTimeSeries.

        :param TimeSeries otherTimeSeries:    TimeSeries instance that will be merged with :py:obj:`self`.

        :return:    Returns a new TimeSeries instance containing the data entries of :py:obj:`self` and otherTimeSeries.
        :rtype:     TimeSeries
        """
        data = self._timeseriesData + otherTimeSeries.to_twodim_list()
        return TimeSeries.from_twodim_list(data)

    def __len__(self):
        """Returns the number of data entries stored in the TimeSeries.

        :return:    Returns an Integer representing the number on data entries stored
            within the TimeSeries.
        :rtype:     integer
        """
        return len(self._timeseriesData)

    def __eq__(self, otherTimeSeries):
        """Returns if :py:obj:`self` and the other TimeSeries are equal.

        TimeSeries are equal to each other if:
            - they contain the same number of entries
            - each data entry in one TimeSeries is also member of the other one.

        :param TimeSeries otherTimeSeries:    TimeSeries instance that is compared with :py:obj:`self`.

        :return:    :py:const:`True` if the TimeSeries objects are equal, :py:const:`False` otherwise.
        :rtype:     boolean
        """
        ## Compare the length of the time series
        if len(self) != len(otherTimeSeries):
            return False

        ## @todo: This can be really cost intensive!
        orgTS  = self.sorted_timeseries()
        compTS = otherTimeSeries.sorted_timeseries()

        for idx in xrange(len(orgTS)):
            ## compare the timestamp
            if orgTS[idx][0] != compTS[idx][0]:
                return False

            ## compare the data
            if orgTS[idx][1] != compTS[idx][1]:
                return False

        ## everything seams to be ok
        return True

    def __ne__(self, otherTimeSeries):
        """Returns if :py:obj:`self` and the other MultiDimensionalTimeSeries are equal."""
        return not self == otherTimeSeries

    def __iter__(self):
        """Returns an iterator that can be used to iterate over the data stored within the TimeSeries.

        :return:    Returns an iterator for the TimeSeries.
        :rtype:     Iterator
        """
        return self._timeseriesData.__iter__()

    def __getitem__(self, index):
        """Returns the item stored at the TimeSeries index-th position.

        :param integer index:    Position of the element that should be returned.
            Starts at 0

        :return:    Returns a list containing [timestamp, data] lists.
        :rtype: list

        :raise:     Raises an :py:exc:`IndexError` if the index is out of range.
        """
        return self._timeseriesData[index]

    def __setitem__(self, index, value):
        """Sets the item at the index-th position of the TimeSeries.

        :param integer index:    Index of the element that should be set.
        :param list value:    A list of the form [timestamp, data]

        :raise:    Raises an :py:exc:`IndexError` if the index is out of range.
        """
        self._timeseriesData[index] = value

    @classmethod
    def convert_timestamp_to_epoch(cls, timestamp, tsformat):
        """Converts the given timestamp into a float representing UNIX-epochs.

        :param string timestamp: Timestamp in the defined format.
        :param string tsformat:    Format of the given timestamp. This is used to convert the
            timestamp into UNIX epochs. For valid examples take a look into
            the :py:func:`time.strptime` documentation.


        :return:    Returns an float, representing the UNIX-epochs for the given timestamp.
        :rtype: float
        """
        return time.mktime(time.strptime(timestamp, tsformat))

    @classmethod
    def convert_epoch_to_timestamp(cls, timestamp, tsformat):
        """Converts the given float representing UNIX-epochs into an actual timestamp.

        :param float timestamp:    Timestamp as UNIX-epochs.
        :param string tsformat:    Format of the given timestamp. This is used to convert the
            timestamp from UNIX epochs. For valid examples take a look into the
            :py:func:`time.strptime` documentation.

        :return:    Returns the timestamp as defined in format.
        :rtype: string
        """
        return time.strftime(tsformat, time.gmtime(timestamp))

    def add_entry(self, timestamp, data):
        """Adds a new data entry to the TimeSeries.

        :param timestamp:    Time stamp of the data.
            This has either to be a float representing the UNIX epochs
            or a string containing a timestamp in the given format.
        :param numeric data:    Actual data value.
        """
        self._normalized = self._predefinedNormalized
        self._sorted     = self._predefinedSorted

        tsformat = self._timestampFormat
        if tsformat is not None:
            timestamp = TimeSeries.convert_timestamp_to_epoch(timestamp, tsformat)

        self._timeseriesData.append([float(timestamp), float(data)])

    def sort_timeseries(self, ascending=True):
        """Sorts the data points within the TimeSeries according to their occurrence inline.

        :param boolean ascending: Determines if the TimeSeries will be ordered ascending or
            descending. If this is set to descending once, the ordered parameter defined in
            :py:meth:`TimeSeries.__init__` will be set to False FOREVER.

        :return:    Returns :py:obj:`self` for convenience.
        :rtype:     TimeSeries
        """
        # the time series is sorted by default
        if ascending and self._sorted:
            return

        sortorder = 1
        if not ascending:
            sortorder = -1
            self._predefinedSorted = False

        self._timeseriesData.sort(key=lambda i: sortorder * i[0])

        self._sorted = ascending

        return self

    def sorted_timeseries(self, ascending=True):
        """Returns a sorted copy of the TimeSeries, preserving the original one.

        As an assumption this new TimeSeries is not ordered anymore if a new value is added.

        :param boolean ascending:    Determines if the TimeSeries will be ordered ascending
            or descending.

        :return:    Returns a new TimeSeries instance sorted in the requested order.
        :rtype:     TimeSeries
        """
        sortorder = 1
        if not ascending:
            sortorder = -1

        data = sorted(self._timeseriesData, key=lambda i: sortorder * i[0])

        newTS = TimeSeries(self._normalized)
        for entry in data:
            newTS.add_entry(*entry)

        newTS._sorted = ascending

        return newTS

    def normalize(self, normalizationLevel="minute", fusionMethod="mean", interpolationMethod="linear"):
        """Normalizes the TimeSeries data points.

        If this function is called, the TimeSeries gets ordered ascending
        automatically. The new timestamps will represent the center of each time
        bucket. Within a normalized TimeSeries, the temporal distance between two consecutive data points is constant.

        :param string normalizationLevel:    Level of normalization that has to be applied.
            The available normalization levels are defined in :py:data:`timeseries.NormalizationLevels`.
        :param string fusionMethod:    Normalization method that has to be used if multiple data entries exist
            within the same normalization bucket. The available methods are defined in :py:data:`timeseries.FusionMethods`.
        :param string interpolationMethod: Interpolation method that is used if a data entry at a specific time
            is missing. The available interpolation methods are defined in :py:data:`timeseries.InterpolationMethods`.

        :raise: Raises a :py:exc:`ValueError` if a normalizationLevel, fusionMethod or interpolationMethod hanve an unknown value.
        """
        ## do not normalize the TimeSeries if it is already normalized, either by
        ## definition or a prior call of normalize(*)
        if self._normalizationLevel == normalizationLevel:
            if self._normalized:    # pragma: no cover
                return

        ## check if all parameters are defined correctly
        if normalizationLevel not in NormalizationLevels:
            raise ValueError("Normalization level %s is unknown." % normalizationLevel)
        if fusionMethod not in FusionMethods:
            raise ValueError("Fusion method %s is unknown." % fusionMethod)
        if interpolationMethod not in InterpolationMethods:
            raise ValueError("Interpolation method %s is unknown." % interpolationMethod)

        ## (nearly) empty TimeSeries instances do not require normalization
        if len(self) < 2:
            self._normalized = True
            return

        ## get the defined methods and parameter
        self._normalizationLevel = normalizationLevel
        normalizationLevel       = NormalizationLevels[normalizationLevel]
        fusionMethod             = FusionMethods[fusionMethod]
        interpolationMethod      = InterpolationMethods[interpolationMethod]

        ## sort the TimeSeries
        self.sort_timeseries()

        ## prepare the required buckets
        start           = self._timeseriesData[0][0]
        end             = self._timeseriesData[-1][0]
        span            = end - start
        bucketcnt       = int(span / normalizationLevel) + 1

        buckethalfwidth = normalizationLevel / 2.0
        bucketstart     = start + buckethalfwidth
        buckets         = [[bucketstart + idx * normalizationLevel] for idx in xrange(bucketcnt)]

        # Step One: Populate buckets
        ## Initialize the timeseries data iterators
        tsdStartIdx = 0
        tsdEndIdx   = 0
        tsdlength   = len(self)

        for idx in xrange(bucketcnt):
            ## get the bucket to avoid multiple calls of buckets.__getitem__()
            bucket = buckets[idx]

            ## get the range for the given bucket
            bucketend   = bucket[0] + buckethalfwidth

            while tsdEndIdx < tsdlength and self._timeseriesData[tsdEndIdx][0] < bucketend:
                tsdEndIdx += 1

            ## continue, if no valid data entries exist
            if tsdStartIdx == tsdEndIdx:
                continue

            ## use the given fusion method to calculate the fusioned value
            values = [i[1] for i in self._timeseriesData[tsdStartIdx:tsdEndIdx]]
            bucket.append(fusionMethod(values))

            ## set the new timeseries data index
            tsdStartIdx = tsdEndIdx

        ## Step Two: Fill missing buckets
        missingCount   = 0
        lastIdx        = 0
        for idx in xrange(bucketcnt):
            ## bucket is empty
            if 1 == len(buckets[idx]):
                missingCount += 1
                continue

            ## This is the first bucket. The first bucket is not empty by definition!
            if idx == 0:
                lastIdx = idx
                continue

            ## update the lastIdx, if none was missing
            if 0 == missingCount:
                lastIdx = idx
                continue

            ## calculate and fill in missing values
            missingValues = interpolationMethod(buckets[lastIdx][1], buckets[idx][1], missingCount)
            for idx2 in xrange(1, missingCount + 1):
                buckets[lastIdx + idx2].append(missingValues[idx2 - 1])

            lastIdx = idx
            missingCount = 0

        self._timeseriesData = buckets

        ## at the end set self._normalized to True
        self._normalized = True

    def is_normalized(self):
        """Returns if the TimeSeries is normalized.

        :return:    Returns :py:const:`True` if the TimeSeries is normalized, :py:const:`False` otherwise.
        :rtype: boolean
        """
        if not self._normalized:
            return self._check_normalization()

        return self._normalized

    def _check_normalization(self):
        """Checks, if the TimeSeries is normalized.

        :return:    Returns :py:const:`True` if all data entries of the TimeSeries have an equal temporal
            distance, :py:const:`False` otherwise.
        """
        lastDistance = None
        distance     = None
        for idx in xrange(len(self) - 1):
            distance = self[idx+1][0] - self[idx][0]

            ## first run
            if lastDistance is None:
                lastDistance = distance
                continue

            if lastDistance != distance:
                return False

            lastDistance = distance

        return True

    def is_sorted(self):
        """Returns if the TimeSeries is sorted.

        :return:    Returns :py:const:`True` if the TimeSeries is sorted ascending, :py:const:`False` in all other cases.
        :rtype: boolean
        """
        return self._sorted

    def apply(self, method):
        """Applies the given ForecastingAlgorithm or SmoothingMethod from the :py:mod:`pycast.methods`
        module to the TimeSeries.

        :param BaseMethod method: Method that should be used with the TimeSeries.
            For more information about the methods take a look into their corresponding documentation.

        :raise:    Raises a StandardError when the TimeSeries was not normalized and hte method requires a
            normalized TimeSeries
        """
        ## check, if the methods requirements are fullfilled
        if method.has_to_be_normalized() and not self._normalized:
            raise StandardError("method requires a normalized TimeSeries instance.")

        if method.has_to_be_sorted():
            self.sort_timeseries()

        return method.execute(self)

    def sample(self, percentage):
        """Samples with replacement from the TimeSeries. Returns the sample and the remaining timeseries.
        The original timeseries is not changed.

        :param float percentage: How many percent of the original timeseries should be in the sample

        :return:    A tuple containing (sample, rest) as two TimeSeries.
        :rtype: tuple(TimeSeries,TimeSeries)

        :raise:    Raises a ValueError if percentage is not in (0.0, 1.0).
        """
        if not (0.0 < percentage < 1.0):
            raise ValueError("Parameter percentage has to be in (0.0, 1.0).")

        cls         = self.__class__
        value_count = int(len(self) * percentage)
        values      = random.sample(self, value_count)

        sample      = cls.from_twodim_list(values)
        rest_values = self._timeseriesData[:]

        for value in values:
            rest_values.remove(value)

        rest = cls.from_twodim_list(rest_values)

        return sample, rest

class MultiDimensionalTimeSeries(TimeSeries):
    """Implements a multi dimensional TimeSeries."""

    def __init__(self, dimensions=1, isNormalized=False, isSorted=False):
        """Initializes the TimeSeries.

        :param integer dimensions:    Number of dimensions the MultiDimensionalTimeSeries contains.
            If dimensions is 1, a normal TimeSeries should be used. The number of dimensions has to
            be 1 at least.
        :param boolean isNormalized:    Within a normalized TimeSeries, all data points
            have the same temporal distance to each other.
            When this is :py:const:`True`, the memory consumption of the TimeSeries might be reduced.
            Also algorithms will probably run faster on normalized TimeSeries.
            This should only be set to :py:const:`True`, if the TimeSeries is really normalized!
            TimeSeries normalization can be forced by executing :py:meth:`TimeSeries.normalize`.
        :param boolean isSorted:    If all data points added to the time series are added
            in their ascending temporal order, this should set to :py:const:`True`.

        :raise:    Raises a :py:exc:`ValueError` if the number of dimensions is smaller than 1.
        """
        super(MultiDimensionalTimeSeries, self).__init__(isNormalized, isSorted)

        dimensions = int(dimensions)
        if dimensions < 1:
            raise ValueError("A MultiDimensionalTimeSeries has to have at least one dimension!.")

        self._dimensionCount = dimensions

    def dimension_count(self):
        """Returns the number of dimensions the MultiDimensionalTimeSeries contains.

        :return:    Number of dimensions contained within the TimeSeries.
        :rtype: integer
        """
        return self._dimensionCount

    def add_entry(self, timestamp, data):
        """Adds a new data entry to the TimeSeries.

        :param timestamp:    Time stamp of the data.
            This has either to be a float representing the UNIX epochs
            or a string containing a timestamp in the given format.
        :param list data:    A list containing the actual dimension values.

        :raise:    Raises a :py:exc:`ValueError` if data does not contain as many dimensions as
            defined in __init__.
        """
        if not isinstance(data, list):
            data = [data]

        if len(data) != self._dimensionCount:
            raise ValueError("data does contain %s instead of %s dimensions.\n   %s" % (len(data), self._dimensionCount, data))

        self._normalized = self._predefinedNormalized
        self._sorted     = self._predefinedSorted

        tsformat = self._timestampFormat
        if tsformat is not None:
            timestamp = TimeSeries.convert_timestamp_to_epoch(timestamp, tsformat)

        self._timeseriesData.append([float(timestamp)] + [float(dimensionValue) for dimensionValue in data])

    def sorted_timeseries(self, ascending=True):
        """Returns a sorted copy of the TimeSeries, preserving the original one.

        As an assumption this new TimeSeries is not ordered anymore if a new value is added.

        :param boolean ascending:    Determines if the TimeSeries will be ordered ascending
            or descending.

        :return:    Returns a new TimeSeries instance sorted in the requested order.
        :rtype:     TimeSeries
        """
        sortorder = 1
        if not ascending:
            sortorder = -1

        data = sorted(self._timeseriesData, key=lambda i: sortorder * i[0])

        newTS = MultiDimensionalTimeSeries(self._dimensionCount, self._normalized)
        for entry in data:
            newTS.add_entry(entry[0], entry[1:])

        newTS._sorted = ascending

        return newTS

    def to_twodim_list(self):
        """Serializes the MultiDimensionalTimeSeries data into a two dimensional list of [timestamp, [values]] pairs.

        :return:    Returns a two dimensional list containing [timestamp, [values]] pairs.
        :rtype:     list
        """
        if self._timestampFormat is None:
            return self._timeseriesData

        datalist = []
        append   = datalist.append
        convert  = TimeSeries.convert_epoch_to_timestamp
        for entry in self._timeseriesData:
            append([convert(entry[0], self._timestampFormat), entry[1:]])

        return datalist

    @classmethod
    def from_twodim_list(cls, datalist, tsformat=None, dimensions=1):
        """Creates a new MultiDimensionalTimeSeries instance from the data stored inside a two dimensional list.

        :param list datalist:    List containing multiple iterables with at least two values.
            The first item will always be used as timestamp in the predefined format,
            the second is a list, containing the dimension values.
        :param string format:    Format of the given timestamp. This is used to convert the
            timestamp into UNIX epochs, if necessary. For valid examples take a look into
            the :py:func:`time.strptime` documentation.
        :param integer dimensions:    Number of dimensions the MultiDimensionalTimeSeries contains.

        :return:    Returns a MultiDimensionalTimeSeries instance containing the data from datalist.
        :rtype:     MultiDimensionalTimeSeries
        """
        ## create and fill the given TimeSeries
        ts = MultiDimensionalTimeSeries(dimensions=dimensions)
        ts.set_timeformat(tsformat)

        for entry in datalist:
            ts.add_entry(entry[0], entry[1])

        ## set the normalization level
        ts._normalized = ts.is_normalized()
        ts.sort_timeseries()

        return ts

    def __add__(self, otherTimeSeries):
        """Creates a new MultiDimensionalTimeSeries instance containing the data of :py:obj:`self` and otherMutliDimensionalTimeSeries.

        :param MultiDimensionalTimeSeries otherTimeSeries:    MultiDimensionalTimeSeries instance that will be merged with :py:obj:`self`.

        :return:    Returns a new TimeSeries instance containing the data entries of :py:obj:`self` and otherTimeSeries.
        :rtype:     MultiDimensionalTimeSeries

        :raise:    Raises a :py:exc:`ValueError` if the number of dimensions of both MutliDimensionalTimeSeries are not equal.
        """
        if not self._dimensionCount == otherTimeSeries.dimension_count():
            raise ValueError("otherMutliDimensionalTimeSeries has to have the same number of dimensions.")

        data = self.to_twodim_list() + otherTimeSeries.to_twodim_list()
        return MultiDimensionalTimeSeries.from_twodim_list(data)

    def __eq__(self, otherTimeSeries):
        """Returns if :py:obj:`self` and the other MultiDimensionalTimeSeries are equal.

        MultiDimensionalTimeSeries are equal to each other if:
            - they contain the same number of entries
            - each data entry in one MultiDimensionalTimeSeries is also member of the other one.
            - they have the same number of dimensions

        :param MultiDimensionalTimeSeries otherTimeSeries:    MultiDimensionalTimeSeries instance that is compared with :py:obj:`self`.

        :return:    :py:const:`True` if the MultiDimensionalTimeSeries objects are equal, :py:const:`False` otherwise.
        :rtype: boolean
        """
        ## Compare the length of the time series
        if len(self) != len(otherTimeSeries):
            return False

        ## compare the number of dimensions:
        if self._dimensionCount != otherTimeSeries.dimension_count():
            return False

        ## @todo: This can be really cost intensive!
        orgTS  = self.sorted_timeseries()
        compTS = otherTimeSeries.sorted_timeseries()

        for idx in xrange(len(orgTS)):
            ## compare the timestamp
            if orgTS[idx][0] != compTS[idx][0]:
                return False

            ## compare the data
            if orgTS[idx][1:] != compTS[idx][1:]:
                return False

        ## everything seams to be ok
        return True

    def __copy__(self):
        """Returns a new clone of the MultiDimensionalTimeSeries.

        :return:    Returns a MultiDimensionalTimeSeries containing the same data and configuration as self.
        :rtype:     MultiDimensionalTimeSeries
        """
        ts = MultiDimensionalTimeSeries.from_twodim_list(self._timeseriesData, dimensions=self._dimensionCount)

        ts._normalizationLevel   = self._normalizationLevel
        ts._normalized           = self._normalized
        ts._sorted               = self._sorted
        ts._predefinedSorted     = self._predefinedSorted
        ts._predefinedNormalized = self._predefinedNormalized
        ts._timestampFormat      = self._timestampFormat

        return ts

    def initialize_from_sql_cursor(self, sqlcursor):
        """Initializes the MultiDimensionalTimeSeries's data from the given SQL cursor.

        You need to set the time stamp format using :py:meth:`MultiDimensionalTimeSeries.set_timeformat`.

        :param SQLCursor sqlcursor:    Cursor that was holds the SQL result for any given
            "SELECT timestamp, value, ... FROM ..." SQL query.

        :return:    Returns the number of entries added to the MultiDimensionalTimeSeries.
        :rtype: integer
        """
        ## initialize the result
        tuples = 0

        ## add the SQL result to the timeseries
        data = sqlcursor.fetchmany()
        while 0 < len(data):
            for entry in data:
                self.add_entry(str(entry[0]), [item for item in entry[1:]])

            data = sqlcursor.fetchmany()

        ## set the normalization level
        self._normalized = self._check_normalization()

        ## return the number of tuples added to the timeseries.
        return tuples

    def to_gnuplot_datafile(self, datafilepath):
        """Dumps the TimeSeries into a gnuplot compatible data file.

        :param string datafilepath:    Path used to create the file. If that file already exists,
            it will be overwritten!

        :return:   Returns :py:const:`True` if the data could be written, :py:const:`False` otherwise.
        :rtype: boolean
        """
        try:
            datafile = file(datafilepath, "wb")
        except Exception:
            return False

        if self._timestampFormat is None:
            self._timestampFormat = _STR_EPOCHS

        datafile.write("## time_as_<%s> value..." % self._timestampFormat)

        convert = TimeSeries.convert_epoch_to_timestamp
        for datapoint in self._timeseriesData:
            timestamp = datapoint[0]
            values = datapoint[1:]
            if format is not None:
                timestamp = convert(timestamp, format)

            datafile.write("%s %s" % (timestamp, " ".join([str(entry) for entry in values])))

        datafile.close()
        return True

    def normalize(self, normalizationLevel="minute", fusionMethod="mean", interpolationMethod="linear"):
        """This is a dummy function, doing nothing.

        :raise: Raises a :py:exc:`NotImplementedError`.

        :note: MutliDimensionalTimeSeries cannot be normalized currently.
        """
        raise NotImplementedError
