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

# required external modules
import unittest
import os

# required modules from pycast
from pycast.common.profileme import profileMe

class ProfileMeDecoratorTest(unittest.TestCase):

    """Test class containing all tests for the @profileMe decorator."""

    def setUp(self):
        """Initializes the environment for each test."""
        self.statfiles = ["statfile1", "statfile2"]

    def tearDown(self):
        """This function gets called after each test function."""
        for statfile in self.statfiles:
            if os.path.isfile(statfile):
                os.remove(statfile)

    def profile_data_creation_test(self):
        """Testing successfull profile data creation."""
        statfile = self.statfiles[0]

        @profileMe(statfile)
        def dummy_func():
            """This is an (nearly) empty dummy function that nees to be profiled.

            The functions evaluates, if the formula for the gaussian sum is correct.
            """
            sumUpTo = 1000

            summedVals = sum(xrange(sumUpTo + 1))
            easySum = (sumUpTo * (sumUpTo + 1)) / 2

            return easySum == summedVals

        booleanVal = dummy_func()

        if not (booleanVal):
            raise AssertionError
        if not (os.path.isfile(statfile)):
            raise AssertionError

    def profile_function_name_test(self):
        """Test the validity of __name__ for any decorated function."""

        statfile = self.statfiles[0]

        @profileMe(statfile)
        def dummy_func():
            """This is an (nearly) empty dummy function that nees to be profiled.

            The functions evaluates, if the formula for the gaussian sum is correct.
            """
            sumUpTo = 1000

            summedVals = sum(xrange(sumUpTo + 1))
            easySum = (sumUpTo * (sumUpTo + 1)) / 2

            return easySum == summedVals

        booleanVal = dummy_func()

        if not (booleanVal):
            raise AssertionError
        if not (dummy_func.__name__ == "dummy_func"):
            raise AssertionError

    def profile_doc_string_test(self):
        """Test the validity of __doc__ for any decorated function."""
        statfile = self.statfiles[0]

        @profileMe(statfile)
        def dummy_func():
            """StupidDocString"""
            sumUpTo = 1000

            summedVals = sum(xrange(sumUpTo + 1))
            easySum = (sumUpTo * (sumUpTo + 1)) / 2

            return easySum == summedVals

        booleanVal = dummy_func()

        if not (booleanVal):
            raise AssertionError
        if not (dummy_func.__doc__ == """StupidDocString"""):
            raise AssertionError
