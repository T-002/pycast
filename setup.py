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