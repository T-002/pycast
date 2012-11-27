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

import time

## some string constants
_STR_EPOCHS = "UNIX-epochs"

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

class TimeSeries(object):
    """A TimeSeries instance stores all relevant data for a real world time series.

    :warning: TimeSeries instances are NOT threadsafe.
    """

    def __init__(self, isNormalized=False, isSorted=False):
        """Initializes the TimeSeries.

        :param Boolean isNormalized:    Within a normalized TimeSeries, all data points
            have the same temporal distance to each other.
            When this is :py:const:`True`, the memory consumption of the TimeSeries might be reduced.
            Also algorithms will probably run faster on normalized TimeSeries.
            This should only be set to :py:const:`True`, if the TimeSeries is realy normalized!
            TimeSeries normalization can be forced by executing :py:meth:`TimeSeries.normalize`.
        :param Boolean isSorted:    If all data points added to the time series are added
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

    def set_timeformat(self, format=None):
        """Sets the TimeSeries global time format.

        :param String format:    Format of the timestamp. This is used to convert the
            timestamp from UNIX epochs when the TimeSeries gets serialized by :py:meth:`TimeSeries.to_json` and 
            :py:meth:`TimeSeries.to_gnuplot_datafile`. For valid examples take a look into the :py:func:`time.strptime`
            documentation.
        """
        self._timestampFormat = format

    def to_gnuplot_datafile(self, datafilepath):
        """Dumps the TimeSeries into a gnuplot compatible data file.

        :param String datafilepath:    Path used to create the file. If that file already exists,
            it will be overwritten!

        :return:   Returns :py:const:`True` if the data could be written, :py:const:`False` otherwise.
        :rtype:    Boolean
        """
        try:
            datafile = file(datafilepath, "wb")
        except:
            return False

        format = self._timestampFormat
        
        formatval = format
        if None == format:
            formatval = _STR_EPOCHS

        datafile.write("## time_as_<%s> value" % formatval)

        convert = TimeSeries.convert_epoch_to_timestamp
        for datapoint in self._timeseriesData:
            timestamp, value = datapoint
            if None != format:
                timestamp = convert(timestamp, format)

            datafile.write("%s %s" % (timestamp, value))

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

    def to_json(self):
        """Returns a JSON representation of the TimeSeries data.

        :return:    Returns a basestring, containing the JSON representation of the current
            data stored within the TimeSeries.
        :rtype:     String
        """
        ## return the simple way if no timestamp format was requested
        format = self._timestampFormat
        if None == self._timestampFormat:
            return "[%s]"% ",".join([str(entry) for entry in self._timeseriesData])

        ## initialize the result
        valuepairs = []
        append     = valuepairs.append
        convert    = TimeSeries.convert_epoch_to_timestamp
        
        for entry in self._timeseriesData:
            append('["%s",%s]' % (convert(entry[0], format), entry[1]))

        ## return the result
        return "[%s]" % ",".join(valuepairs)

    @classmethod
    def from_json(cls, json, format=None):
        """Creates a new TimeSeries instance from the given json string.

        :param String json:    JSON string, containing the time series data. This
            should be a string created by :py:meth:`TimeSeries.to_json`.
        :param String format:    Format of the given timestamps. This is used to convert the
            timestamps into UNIX epochs, if set. For valid examples take a look into
            the :py:func:`time.strptime` documentation.

        :return:    Returns a TimeSeries instance containing the data.
        :rtype:     TimeSeries

        :warning:    This is probably an unsafe version! Only use it with JSON strings created by 
            :py:meth:`TimeSeries.to_json`.
            All assumtions regarding normalization and sort order will be ignored and 
            set to default.
        """
        ## create and fill the given TimeSeries
        ts = TimeSeries()
        ts.set_timeformat(format)

        for entry in eval(json):
            ts.add_entry(*entry)

        ## set the normalization level
        ts._normalized = ts.check_normalization()
        ts.sort_timeseries()

        return ts

    def to_twodim_list(self):
        """Serializes the TimeSeries data into a two dimensional list of [timestamp, value] pairs.

        :return:    Returns a two dimensional list containing [timestamp, value] pairs.
        :rtype:     List
        """
        format = self._timestampFormat

        if None == format:
            return self._timeseriesData

        datalist = []
        append   = datalist.append
        convert  = TimeSeries.convert_epoch_to_timestamp
        for entry in self._timeseriesData:
            append([convert(entry[0], format), entry[1]])

        return datalist

    @classmethod
    def from_twodim_list(cls, datalist, format=None):
        """Creates a new TimeSeries instance from the data stored inside a two dimensional list.

        :param List datalist:    List containing multiple iterables with at least two values.
            The first item will always be used as timestamp in the predefined format,
            the second represents the value. All other items in those sublists will be ignored.
        :param String format:    Format of the given timestamp. This is used to convert the
            timestamp into UNIX epochs, if necessary. For valid examples take a look into
            the :py:func:`time.strptime` documentation.

        :return:    Returns a TimeSeries instance containing the data from datalist.
        :rtype:     TimeSeries
        """
        ## create and fill the given TimeSeries
        ts = TimeSeries()
        ts.set_timeformat(format)

        for entry in datalist:
            ts.add_entry(*entry[:2])

        ## set the normalization level
        ts._normalized = ts.check_normalization()
        ts.sort_timeseries()  

        return ts

    def initialize_from_sql_cursor(self, sqlcursor):
        """Initializes the TimeSeries's data from the given SQL cursor.

        You need to set the time stamp format using :py:meth:`TimeSeries.set_timeformat`.

        :param SQLCursor sqlcursor:    Cursor that was holds the SQL result for any given
            "SELECT timestamp, value, ... FROM ..." SQL query.
            Only the first two attributes of the SQL result will be used.

        :return:    Returns the number of entries added to the TimeSeries.
        :rtype:     Integer
        """
        ## initialize the result
        tuples = 0

        ## add the SQL result to the timeseries
        data = sqlcursor.fetchmany()
        while 0 < len(data):
            for entry in data:
                self.add_entry(*entry[:2])

            data = sqlcursor.fetchmany()

        ## set the normalization level
        self._normalized = self.check_normalization
        
        ## return the number of tuples added to the timeseries.
        return tuples

    def __str__(self):
        """Returns a string representation of the TimeSeries.

        :return:    Returns a string representing the TimeSeries in the format:
            
            "TimeSeries([timestamp, data], [timestamp, data], [timestamp, data])".
        :rtype:     String
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
        :rtype:     Integer
        """
        return len(self._timeseriesData)

    def __eq__(self, otherTimeSeries):
        """Returns if :py:obj:`self` and the other TimeSeries are equal.

        TimeSeries are equal to each other if:
            - they contain the same number of entries
            - each data entry in one TimeSeries is also member of the other one.

        :param TimeSeries otherTimeSeries:    TimeSeries instance that is compared with :py:obj:`self`.

        :return:    :py:const:`True` if the TimeSeries objects are equal, :py:const:`False` otherwise.
        :rtype:     Boolean
        """
        ## Compare the length of the time series
        if len(self) != len(otherTimeSeries):
            return False

        ## @todo: This can be realy cost intensive!
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

    def __iter__(self):
        """Returns an iterator that can be used to iterate over the data stored within the TimeSeries.

        :return:    Returns an iterator for the TimeSeries.
        :rtype:     Iterator
        """
        return self._timeseriesData.__iter__()

    def __getitem__(self, index):
        """Returns the item stored at the TimeSeries index-th position.

        :param Integer index:    Position of the element that should be returned.
            Starts at 0

        :return:    Returns a list containing [timestamp, data] lists.
        :rtype:     List

        :raise:     Raises an :py:exc:`IndexError` if the index is out of range.
        """
        return self._timeseriesData[index]

    def __setitem__(self, index, value):
        """Sets the item at the index-th position of the TimeSeries.

        :param Integer index:    Index of the element that should be set.
        :param List value:    A list of the form [timestamp, data]

        :raise:    Raises an :py:exc:`IndexError` if the index is out of range.
        """
        self._timeseriesData[index] = value

    @classmethod
    def convert_timestamp_to_epoch(cls, timestamp, format):
        """Converts the given timestamp into a float representing UNIX-epochs.

        :param String timestamp: Timestamp in the defined format.
        :param String format:    Format of the given timestamp. This is used to convert the
            timestamp into UNIX epochs. For valid examples take a look into
            the :py:func:`time.strptime` documentation.


        :return:    Returns an float, representing the UNIX-epochs for the given timestamp.
        :rtype:     Float
        """
        return time.mktime(time.strptime(timestamp, format))

    @classmethod
    def convert_epoch_to_timestamp(cls, timestamp, format):
        """Converts the given float representing UNIX-epochs into an actual timestamp.

        :param Float timestamp:    Timestamp as UNIX-epochs.
        :param String format:    Format of the given timestamp. This is used to convert the
            timestamp from UNIX epochs. For valid examples take a look into the 
            :py:func:`time.strptime` documentation.

        :return:    Returns the timestamp as defined in format.
        :rtype:     String
        """
        return time.strftime(format, time.localtime(timestamp))

    def add_entry(self, timestamp, data):
        """Adds a new data entry to the TimeSeries.

        :param timestamp:    Time stamp of the data.
            This has either to be a float representing the UNIX epochs
            or a string containing a timestamp in the given format.
        :param Numeric data:    Actual data value.
        """
        self._normalized = self._predefinedNormalized
        self._sorted     = self._predefinedSorted

        format = self._timestampFormat
        if None != format:
            timestamp = TimeSeries.convert_timestamp_to_epoch(timestamp, format)

        self._timeseriesData.append([float(timestamp), float(data)])

    def sort_timeseries(self, ascending=True):
        """Sorts the data points within the TimeSeries according to their occurence inline.

        :param Boolean ascending: Determines if the TimeSeries will be ordered ascending or
            decending. If this is set to decending once, the ordered parameter defined in 
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

        As an assumtion this new TimeSeries is not ordered anymore if a new value is added.

        :param Boolean ascending:    Determines if the TimeSeries will be ordered ascending
            or decending.

        :return:    Returns a new TimeSeries instance sorted in the requested order.
        :rtype:     TimeSeries
        """
        sortorder = 1
        if False == ascending:
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

        :param String normalizationLevel:    Level of normalization that has to be applied.
            The available normalization levels are defined in :py:data:`timeseries.NormalizationLevels`.
        :param String fusionMethod:    Normalization method that has to be used if multiple data entries exist
            within the same normalization bucket. The available methods are defined in :py:data:`timeseries.FusionMethods`.
        :param String interpolationMethod: Interpolation method that is used if a data entry at a specific time
            is missing. The available interpolation methods are defined in :py:data:`timeseries.InterpolationMethods`.

        :raise: Raises a :py:exc:`ValueError` if a normalizationLevel, fusionMethod or interpolationMethod hanve an unknown value.
        """
        ## do not normalize the TimeSeries if it is already normalized, either by
        ## definition or a prior call of normalize(*)
        if self._normalizationLevel == normalizationLevel:
            if self._normalized:    # pragma: no cover
                return

        ## check if all parameters are defined correctly
        if not normalizationLevel in NormalizationLevels:
            raise ValueError("Normalization level %s is unknown." % normalizationLevel)
        if not fusionMethod in FusionMethods:
            raise ValueError("Fusion method %s is unknown." % fusionMethod)
        if not interpolationMethod in InterpolationMethods:
            raise ValueError("Interpolation method %s is unknown." % interpolationMethod)

        ## (nearly) empty TimeSeries instances do not require normalization
        if len(self) < 2:
            self._normalized = True
            return

        ## get the defined methods and parameter
        normalizationLevelString = normalizationLevel
        normalizationLevel       = NormalizationLevels[normalizationLevel]
        fusionMethod             = FusionMethods[fusionMethod]
        interpolationMethod      = InterpolationMethods[interpolationMethod]

        ## sort the TimeSeries
        self.sort_timeseries()

        ## prepare the required buckets
        start           = self._timeseriesData[0][0]
        end             = self._timeseriesData[-1][0]
        span            = end - start
        bucketcnt       = int(span / normalizationLevel)+ 1

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
        self._normalizationLevel = normalizationLevelString

    def is_normalized(self):
        """Returns if the TimeSeries is normalized.

        :return:    Returns :py:const:`True` if the TimeSeries is normalized, :py:const:`False` otherwise.
        :rtype:     Boolean
        """
        return self._normalized

    def check_normalization(self):
        """Checks, if the TimeSeries is normalized.

        :return:    Returns :py:const:`True` if all data entries of the TimeSeries have an equal temporal
            distance, :py:const:`False` otherwise.
        """
        lastDistance = None
        distance     = None
        for idx in xrange(len(self) - 1):
            distance = self[idx+1][0] - self[idx][0]

            ## first run
            if None == lastDistance:
                lastDistance = distance
                continue

            if lastDistance != distance:
                return False

            lastDistance = distance

        return True

    def is_sorted(self):
        """Returns if the TimeSeries is sorted.

        :return:    Returns :py:const:`True` if the TimeSeries is sorted ascending, :py:const:`False` in all other cases.
        :rtype:     Boolean
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
