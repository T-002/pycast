# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# Copyright (c) 2012-2019 Christian Schwarz
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

import os
import pytest

from pycast.common.profiling import profile_me


class TestProfileMeDecorator:
    """Test class containing all tests for the @profile_me decorator."""

    def setup(self):
        """Initializes the environment for each test."""
        self.stat_file = f"{os.path.dirname(__file__)}/../_build/tests/statfile1.stats"

    def teardown(self):
        """This function gets called after each test function."""
        if os.path.isfile(self.stat_file):
            os.remove(self.stat_file)

    def test_profile_data_creation(self):
        """Tests if the profiling file gets written to the given location."""
        @profile_me(self.stat_file)
        def calculate_gauss_sum():
            """This is an (nearly) empty dummy function that nees to be profiled.

            The functions evaluates, if the formula for the gaussian sum is correct.
            """
            sum_up_to = 1000

            brute_force_sum = sum(range(sum_up_to + 1))
            gauss_sum = (sum_up_to * (sum_up_to + 1)) / 2

            return gauss_sum == brute_force_sum

        assert calculate_gauss_sum(), "Dummy function did not return True. Please check the dummy."
        assert os.path.isfile(self.stat_file), f"Data file was not created at *{self.stat_file}*."

    def test_profile_function_name(self):
        """Test the validity of __name__ for any decorated function."""
        @profile_me(self.stat_file)
        def return_42():
            """This is a completely useless dummy function.

            Returns:
                int: Always returns 42.
            """
            return 42

        assert 42 == return_42(), "Dummy function did not return the correct answer."
        assert "return_42" == return_42.__name__

    def test_profile_doc_string(self):
        """Test the validity of __doc__ for any decorated function."""
        @profile_me(self.stat_file)
        def dummy_func():
            """StupidDocString"""

        assert """StupidDocString""" == dummy_func.__doc__
