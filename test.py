from pycast.common.timeseries import TimeSeries
#
#ts1 = TimeSeries()
#ts1.add_entry(0.0, 0.0)
#ts1.add_entry(0.1, 0.2)
#
#print ts1
#print str(ts1)
#print ts1.__repr__()
#
#ts2 = ts1.sorted_timeseries()
#assert(ts1 == ts2)
#ts2.add_entry(0.11, 0.2)
#assert(ts1 != ts2)
#print "TimeSeries equal comparison seams to work."
#
#ts1.normalize()
#
#from pycast.common.helper import linear_interpolation
#
#v1, v2 = 1, 3
#
#result = linear_interpolation(v1,v2,1)
#assert(result == [2.0])
#
#v1, v2 = 1, 4
#result =linear_interpolation(v1,v2,2)
#assert(result == [2.0, 3.0])
#
#v1, v2 = 0, 5
#result =linear_interpolation(v1,v2,4)
#assert(result == [1.0, 2.0, 3.0, 4.0])
#
#from pycast.common.timeseries import TimeSeries
#ts1 = TimeSeries()
#ts1.add_entry(0.0, 0.0)
#ts1.add_entry(1.0, 0.8)
#ts1.add_entry(1.1, 0.9)
#ts1.add_entry(1.2, 1.3)
#ts1.add_entry(2.0, 2.0)
#
#ts1.normalize("second", "average", "linear")
#print ts1
#
#from pycast.common.timeseries import TimeSeries
#ts1 = TimeSeries()
#ts1.add_entry(0.0, 0.0)
#ts1.add_entry(1.0, 0.8)
#ts1.add_entry(2.1, 0.9)
#ts1.add_entry(3.2, 1.3)
#ts1.add_entry(4.0, 2.0)
#
#from pycast.methods.simplemovingaverage import SimpleMovingAverage
#sma = SimpleMovingAverage(3)
#ts1.normalize("second")
#print ts1.apply(sma)
#
#from pycast.methods.exponentialsmoothing import ExponentialSmoothing
#es = ExponentialSmoothing(0.1, 2)
#ts1.normalize("second")
#
#sts = ts1.apply(es)
#assert(len(ts1) + 1 == len(sts))
#print "Exponential smoothed timeseries contains an additional value :)"
#print ts1
#print sts
#
#from pycast.methods.exponentialsmoothing import HoltMethod
#hm  = HoltMethod(smoothingFactor=0.1, trendSmoothingFactor=0.5, valuesToForecast=3)
#fts = ts1.apply(hm)
#assert(len(fts) == len(ts1) + 2)
#print "Holt's method is working"

import sqlite3
con = sqlite3.connect("bin/examples/energy.db")
cur = con.cursor()
cur.execute("""SELECT timestamp, curPower FROM Energy""")

ts = TimeSeries()
ts.initialize_from_sql_cursor(cur)
print ts
