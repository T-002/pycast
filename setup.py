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
from distutils.core import setup
from setuptools     import find_packages

setup(
    name             = "pycast",
    version          = "v0.1.2-alpha",
    author           = "Christian Schwarz",
    author_email     = "pixeldreck@gmail.com",
    packages         = find_packages(exclude=["tests"]),
    url              = "https://github.com/T-002/pycast",
    description      = "A Forecasting and Smoothing Library",
    long_description = open("README.rst").read(),
    download_url     = "https://github.com/T-002/pycast.git",
    scripts          = ["setup.py"],
    requires         = [],
    classifiers      = ["Development Status :: 3 - Alpha",
                        "Intended Audience :: Education",
                        "Intended Audience :: Science/Research",
                        "License :: OSI Approved :: MIT License",
                        "Topic :: Database",
                        "Topic :: Education",
                        "Topic :: Scientific/Engineering :: Mathematics",
                        "Topic :: Scientific/Engineering :: Information Analysis"
    ]
)