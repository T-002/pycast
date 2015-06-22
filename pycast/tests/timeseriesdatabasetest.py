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

# Tests concerning the database connection of pycast.common.TimeSeries
# SQLite is used for connector tests

# required external modules
import unittest, random, sqlite3

# required modules from pycast
from pycast.common.timeseries import TimeSeries, MultiDimensionalTimeSeries

class DatabaseConnectorTest(unittest.TestCase):

    """Testclass for all database connection related tests."""

    def setUp(self):
        """Initializes the environment for each test."""
        self._db = sqlite3.connect(":memory:")
        self.add_data_into_db(self._db, random.randint(100,10000))

    def tearDown(self):
        """This function gets called after each test function."""
        self._db.close()
        del self._db

    def add_data_into_db(self, database, numberOfTuples):
        """Inserts a numberOfTuples tuples into the given database.

        This automatically creates a table called TestTable with the following schema:
            timestamp REAL
            value     REAL
            junk_one  REAL
            junk_two  TEXT

        The time stamps will be inserted as an ordered sequence.

        @param database dbapi2.connection Instance for the used database.
        @param numberOfTuples Number of tuples that have to be created.
        """
        # create the test table
        cur = database.cursor()
        cur.execute("""
            CREATE TABLE TestTable(
                timestamp REAL,
                value     REAL,
                junk_one  REAL,
                junk_two  TEXT
            )
            """)
        database.commit()

        # initialize all required values
        timestamp = 0
        junk_two = ["test"]
        tuples = []
        append = tuples.append

        # create the tuples
        for item in xrange(numberOfTuples):
            timestamp += random.random()
            value     = random.random() * 1000
            junkOne   = random.random()
            junkTwo   = random.choice(junk_two)

            append([timestamp, value,junkOne, junkTwo])

        # insert the tuples into the database
        cur.executemany("""INSERT INTO TestTable VALUES (?,?,?,?)""", tuples)
        database.commit()

    def select_to_many_attributes_test(self):
        """SELECT timestamp, value, junk, FROM TestTable

        This function tests if statements like

        SELECT timestamp, value, junk, ... FROM

        can be used to initialize a TimeSeries instance. TimeSeries should therefore only
        take the first two attributes for data initialization, regardless of their names.
        """
        # read the number of rows from the database
        cur = self._db.cursor().execute("""SELECT COUNT(*) from TestTable""")
        nbrOfTuples = cur.fetchall()[0][0]

        # initialize a TimeSeries instance from a database cursor
        cur = self._db.cursor().execute("""SELECT timestamp, value, junk_one, junk_two FROM TestTable""")
        ts = TimeSeries()
        ts.initialize_from_sql_cursor(cur)

        # check if all values of the database got inserted into the TimeSeries
        assert len(ts) == nbrOfTuples

    def select_star_test(self):
        """SELECT * FROM TestTable

        This function tests if statements like

        SELECT * FROM

        can be used to initialize a TimeSeries instance. TimeSeries should therefore only
        take the first two attributes for data initialization, regardless of their names.
        """
        # read the number of rows from the database
        cur = self._db.cursor().execute("""SELECT COUNT(*) from TestTable""")
        nbrOfTuples = cur.fetchall()[0][0]

        # initialize a TimeSeries instance from a database cursor
        cur = self._db.cursor().execute("""SELECT * FROM TestTable""")
        ts = TimeSeries()
        ts.initialize_from_sql_cursor(cur)

        # check if all values of the database got inserted into the TimeSeries
        assert len(ts) == nbrOfTuples

    def multidimensionaltimeseries_test(self):
        """Test the initialization of the MultiDimensionalTimeSeries."""
        # read the number of rows from the database
        cur = self._db.cursor().execute("""SELECT COUNT(*) from TestTable""")
        nbrOfTuples = cur.fetchall()[0][0]

        # initialize a TimeSeries instance from a database cursor
        cur = self._db.cursor().execute("""SELECT timestamp, value, junk_one FROM TestTable""")
        ts = MultiDimensionalTimeSeries(dimensions=2)
        ts.initialize_from_sql_cursor(cur)

        # check if all values of the database got inserted into the TimeSeries
        assert len(ts) == nbrOfTuples

    def check_for_consistency_test(self):
        """Tests if database initialization and manual initialization create equal TimeSeries instances."""
        # read the number of rows from the database
        cur = self._db.cursor().execute("""SELECT COUNT(*) from TestTable""")
        nbrOfTuples = cur.fetchall()[0][0]

        # SQL extraction statement
        sqlstmt = """SELECT timestamp, value FROM TestTable ORDER BY timestamp ASC"""

        # Initialize one TimeSeries instance manually
        tsManual = TimeSeries()
        data     = self._db.cursor().execute(sqlstmt).fetchall()
        for entry in data:
            tsManual.add_entry(str(entry[0]), entry[1])

        # Initialize one TimeSeries from SQL cursor
        tsAuto = TimeSeries()
        tsAuto.initialize_from_sql_cursor(self._db.cursor().execute(sqlstmt))

        # check if those TimeSeries are equal
        assert (nbrOfTuples == len(tsManual))
        assert (nbrOfTuples == len(tsAuto))
        assert (len(tsManual) == len(tsAuto))
        assert (tsManual == tsAuto)
