Release Notes
=============
v0.2.0-alpha, 2019-XX-XX
------------------------
This is a a general rebuild and massive refactoring of pycast.

Things included in this version:

  * *Python 3.7* - pycast makes use of the up-to-date Python features.
    Python 3.7 will now also be the minimum required version
  * *Docker* - pycast comes with a preconfigured ``Dockerfile`` to ease development a lot
  * *CircleCI* - Switched to using CircleCI for automated CI testing
  * *py.test* - The test runner was updated to use py.test, even if not all old tests have been refactored
    to make use of the additional functionality.
  * General PEP-8 compliance (except for line length of 80 characters)

The following features have been removed from pycast:
  * removed *nosetests* support

The following components got a larger refactoring/renaming:
  * ``pycast.common.profileme`` got refactored. The functionality can now be found in
    ``pycast.common.profiling``. The decorator got renamed to ``profile_me``.


v0.1.5-alpha, 2015-06-22
------------------------
Beautified code using landscape.ios recommendations.

v0.1.5-alpha, 2015-03-15
------------------------
reintegration done, OpenCL support

v0.1.4-alpha, 2013-03-15
------------------------
reintegration of external project branch started

v0.1.3-alpha, 2012-12-19
------------------------
Implemented @optimized and created basic example for implementing and integrating C(++) based methods in pycast

v0.1.2-alpha, 2012-11-29
------------------------
unifying information for package release

v0.1.1-alpha, 2012-11-29
------------------------
setup script finalized

v0.0.10-prealpha, 2012-11-29
----------------------------
MASE, Examples

v0.0.9-prealpha, 2012-11-18
---------------------------
GridSearch Optimization

v0.0.8-prealpha, 2012-11-18
---------------------------
Error Values, Sphinx documentation

v0.0.7-prealpha, 2012-11-11
---------------------------
First Error measures implemented

v0.0.6-prealpha, 2012-11-01
---------------------------
Started implementation of error measures

v0.0.5-prealpha, 2012-10-20
---------------------------
Included test suite with code coverage into pycast

v0.0.4-prealpha, 2012-10-28
---------------------------
Major performance improvement, while reducing the scale out capabilities

v0.0.3-prealpha, 2012-10-27
---------------------------
Added profileMe decorator and database support

v0.0.2-prealpha, 2012-10-24
---------------------------
Added Exponential Smoothing and Holt Forecast methods

v0.0.1-prealpha, 2012-10-23
---------------------------
SMA method implemented

v0.0.0-prealpha, 2012-10-14
---------------------------
Initial release will follow soon.
