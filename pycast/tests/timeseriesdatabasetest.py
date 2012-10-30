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

## Tests concerning the database connection of pycast.common.TimeSeries
## SQLite is used for connector tests

from nose import with_setup
import unittest


class DatabaseConnectorTest(unittest.TestCase):
    """Testclass for all database connection relevant tests."""

    def __init__(self):
        """Initializes the DatabaseConnectorTest.

        The sample database is populated within this function.
        """
        super(DatabaseConnectorTest, self).__init__()

    def setUp(self):
        """Initializes the environment for each test."""

    def tearDown(self):
        """This function gets called after each test funtion."""

    @with_setup(setUp, tearDown)
    def sampleTest(self):
        """This function tests nothing.

        It is only used to demonstrate the signature for possible tests.
        """

#def db_run():
#    import sqlite3
#    con = sqlite3.connect("bin/examples/energy.db")
#    cur = con.cursor()
#    cur.execute("""SELECT timestamp, curPower FROM Energy""")
#    
#    ts = TimeSeries()
#    ts.initialize_from_sql_cursor(cur)
#    print "Length: %s" % len(ts)
#    from pycast.methods.exponentialsmoothing import HoltMethod
#    hm  = HoltMethod(smoothingFactor=0.1, trendSmoothingFactor=0.5, valuesToForecast=10)
#    fts = ts.apply(hm)
#    print "Length: %s" % len(ts)
#    
#    assert(len(ts) + 9 == len(fts))
#    print "Holt's method is working"    
#
#db_run()
#
#import pstats
#p = pstats.Stats("statfile3.cstats")
#p.strip_dirs().sort_stats("cumulative").print_stats()