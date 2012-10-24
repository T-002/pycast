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

## Fusion methods that can be used to fusionate multiple data points within the same time bucket.
FusionMethods = {
    "average": lambda l: sum(l) / len(l),
    "median":  lambda l: sorted(l)[len(l)//2]
}

## Interpolation methods that can be used for interpolation missing data points.
from helper import linear_interpolation
InterpolationMethods = {
    "linear": linear_interpolation
}

class TimeSeries(object):
    """Represents the base class for all time series data."""

    def __init__(self, normalized=False, ordered=False):
        """Initializes the TimeSeries.

        @param normalized Within a normalized TimeSeries, all data points
                          have the same temporal distance to each other.
                          When this is True, the memory consumption of the
                          TimeSeries might be reduced. Also some algorithms
                          will probably run faster on normalized TimeSeries.
                          This should only be set to True, if the TimeSeries
                          is realy normalized!
                          TimeSeries normalization can be forced, by executing
                          normalize().
        @param ordered    If all data points added to the time series are added
                          in their ascending temporal order, this should set to True.
        """
        super(TimeSeries, self).__init__()
        self._normalized           = normalized
        self._predefinedNormalized = normalized

        self._sorted               = ordered
        self._predefinedSorted     = ordered

        self._timeseriesData = []

    def __str__(self):
        """Returns a string representation of the TimeSeries.

        @return Returns a string representing the TimeSeries in the format:
                TimeSeries([timestamp, data], [timestamp, data], [timestamp, data]).
        """
        return """TimeSeries(%s)""" % ",".join([str(entry) for entry in self._timeseriesData])

    def to_gnuplot_datafile(self, datafilepath, format=None):
        """Dumps the TimeSeries into a gnuplot compatible data file.

        @param datafilepath Path used to create the file. If that file already exists, it will be overwritten!
        @param format    Format of the timestamp. For valid examples take a look into the
                         time.strptime() documentation. If format is set to None, UNIX-epochs will be used.

        @return Returns True if the data could be written, False otherwise.
        """
        try:
            datafile = file(datafilepath, "wb")
        except:
            return False
        
        formatval = format
        if None == format:
            formatval = _STR_EPOCHS

        datafile.write("## time_as_<%s> value" % formatval)

        for datapoint in self._timeseriesData:
            timestamp, value = datapoint
            if None != format:
                timestamp = self._epoch_to_timestamp(timestamp, format)

            datafile.write("%s %s" % (timestamp, value))

        datafile.close()
        return True

    def to_json(self):
        """Returns a JSON representation of the TimeSeries data.

        @return Returns a basestring, containing the JSON representation of the current
        data stored within the TimeSeries.
        """
        return """{[%s]}""" % ",".join([str(entry) for entry in self._timeseriesData])

    @classmethod
    def from_json(self, jsonBaseString):
        """Creates a new TimeSeries instance from the given json string.

        @param jsonBaseString JSON string, containing the time series data. This
                              should be a string created by to_json().

        @return Returns a TimeSeries instance containing the data.

        @todo This is an unsafe version! Only use it with the original version.
              All assumtions regarding normalization and sort order will be ignored
              and set to default.
        """
        ## remove the JSON encapsulation
        jsonString = jsonBaseString[1:-1]

        ## create and fill the given TimeSeries
        ts = TimeSeries()
        for entry in eval(jsonString):
            ts.add_entry(*entry)

        return ts

    def __len__(self):
        """Returns the number of data entries that are part of the time series.

        @return Returns an Integer representing the number on data entries stored within the TimeSeries.
        """
        return len(self._timeseriesData)

    def __eq__(self, otherTimeSeries):
        """Returns if the TimeSeries equal another one.

        TimeSeries are equal to each other if:
            - they contain the same number of entries
            - that each data entry in one TimeSeries is also member of the other one.

        The sort order within the TimeSeries datapoints does not matter!

        @return True if the TimeSeries objects are equal, False otherwise.
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
        """Returns an iterator to the TimeSeries stored data.

        @return Returns an iterator for the TimeSeries.
        """
        return self._timeseriesData.__iter__()

    def __getitem__(self, index):
        """Returns the item stored at the TimeSeries index-th position.

        @param index Position of the element that should be returned.
                     Starts at 0

        @return Returns a list consisting of [timestamp, data].

        @exception IndexError is the index is out of range.
        """
        return self._timeseriesData[index]

    def __setitem__(self, index, value):
        """Sets the item at the index-th position of the TimeSeries.

        @param index Index of the element that should be set.
        @param value A list of the form [timestamp, data]

        @exception IndexError if the index is out of range.
        """
        self._timeseriesData[idx] = value

    def _convert_timestamp_to_epoch(self, timestamp, format):
        """Converts the given timestamp into a float representing UNIX-epochs.

        @param timestamp Timestamp in the defined format.
        @param format    Format of the timestamp. For valid examples take a look into the
                         time.strptime() documentation.

        @return Returns an float, representing the UNIX-epochs for the given timestamp.
        """
        return time.mktime(time.strptime(timestamp, format))

    def _convert_epoch_to_timestamp(self, timestamp, format):
        """Converts the given float representing UNIX-epochs into an actual timestamp.

        @param timestamp Timestamp as UNIX-epochs.
        @param format    Format of the timestamp. For valid examples take a look into the
                         time.strptime() documentation.

        @return Returns an timestamp as defined by format. 
        """
        return time.strftime(format, time.localtime(timestamp))

    ## @todo: only floats as data for now. (2012-10-09 Christian)
    def add_entry(self, timestamp, data, format="%Y-%m-%d_%H:%M"):
        """Adds a new data entry to the TimeSeries.

        @param timestamp Time stamp of the datas occurence.
                         This has either to be a float representing the UNIX epochs
                         or a string containing a timestamp in the given format.
        @param data      Data points information.
                         This has to be a float for now.
        @param format    Format of the given timestamp. This is used to convert the
                         timestamp into UNIX epochs, if necessary. For valid examples
                         take a look into the time.strptime() documentation.
        """
        self._normalized = self._predefinedNormalized
        self._sorted     = self._predefinedSorted

        if isinstance(timestamp, basestring):
            timestamp = self._convert_timestamp_to_epoch(timestamp, format)

        self._timeseriesData.append([timestamp, data])

    def sort_timeseries(self, ascending=True):
        """Sorts the data points within the TimeSeries according to their occurence inline.

        @param ascending Determines if the TimeSeries will be ordered ascending or decending.
                         If this is set to decending once, the ordered parameter defined in
                         __init__() will be set to False FOREVER.
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

    def sorted_timeseries(self, ascending=True):
        """Returns a sorted copy of the TimeSeries, preserving the original one.

        As an assumtion this new TimeSeries is not ordered anymore by default.

        @param ascending Determines if the TimeSeries will be ordered ascending or decending.

        @return Returns a new TimeSeries instance sorted in the requested order.
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

    def normalize(self, normalizationLevel="minute", fusionMethod="average", interpolationMethod="linear"):
        """Normalizes the TimeSeries data points.

        If this function is called, the TimeSeries gets ordered ascending automatically.
        The new timestamps will represent the center of each time bucket.

        @param normalizationLevel Level of normalization that has to be applied.
                                  The available normalization levels are defined
                                  in timeseries.NormalizationLevels.
        @param method Normalization method that has to be used if multiple data entries
                      exist within the same normalization bucket.
                      The available methods are defined in timeseries.FusionMethods.
        @param interpolation Interpolation method that is used if a data entry at a specific
                             time is missing.
                             The available interpolation methods are defined in
                             timeseries.InterpolationMethods.
        """
        ## do not normalize the TimeSeries if it is already normalized, either by definition or a prior
        ## call of normalize(*)
        if self._normalized:
            return

        ## check if all parameters are defined correctly
        if not normalizationLevel in NormalizationLevels:
            print "Normalization level %s is unknown." % normalizationLevel
            return
        if not fusionMethod in FusionMethods:
            print "Fusion method %s is unknown." % fusionMethod
            return
        if not interpolationMethod in InterpolationMethods:
            print "Interpolation method %s is unknown." % interpolationMethod
            return

        ## get the defined methods and parameter
        normalizationLevel  = NormalizationLevels[normalizationLevel]
        fusionMethod        = FusionMethods[fusionMethod]
        interpolationMethod = InterpolationMethods[interpolationMethod]

        ## sort the TimeSeries
        self.sort_timeseries()

        ## prepare the required buckets
        start           = self._timeseriesData[0][0]
        end             = self._timeseriesData[-1][0]
        span            = end - start
        bucketcnt       = span / normalizationLevel

        ## add a bucket, if the last value is at the end of a bucket
        if bucketcnt != int(bucketcnt):
            bucketcnt += 1

        bucketcnt = int(bucketcnt)

        buckethalfwidth = normalizationLevel / 2.0
        bucketstart     = start + buckethalfwidth
        buckets         = [[bucketstart + idx * normalizationLevel] for idx in xrange(bucketcnt)]

        ## Step One: Populate buckets
        for idx in xrange(bucketcnt):
            ## get all valid data entries for the given bucket
            bucketstart = buckets[idx][0] - buckethalfwidth
            bucketend   = buckets[idx][0] + buckethalfwidth
            values = filter(lambda i: bucketstart <= i[0] < bucketend, self._timeseriesData)

            ## continue, if no valid data entries exist
            if 0 == len(values):
                continue

            ## use the given fusion method to calculate the fusioned value
            values = [i[1] for i in values]
            buckets[idx].append(fusionMethod(values))

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

        @return Returns True if the TimeSeries is normalized, False otherwise.
        """
        return self._normalized

    def apply(self, method):
        """Applies the given ForecastingAlgorithm or SmoothingMethod from the pycast.forecasting and
        pycast.smoothingmodule to the TimeSeries.

        @param method Method that should be used with the TimeSeries.
                      For more information about the methods take a look into
                      their corresponding documentation.
        """
        ## sort and normalize, if necessary
        if method.has_to_be_normalized():
            self.normalize()
        elif method.has_to_be_sorted():
            self.sort_timeseries()

        return method.execute(self)
