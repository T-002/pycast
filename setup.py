from distutils.core import setup
from setuptools     import find_packages

setup(
    name             = "pycast",
    version          = "v0.1.1-alpha",
    author           = "Christian Schwarz",
    author_email     = "pixeldreck@gmail.com",
    packages         = find_packages(exclude=["tests"]),
    url              = "https://github.com/T-002/pycast",
    license          = "LICENSE.txt",
    description      = "A Python Forecasting and Smoothing Library",
    long_description = open("README.rst").read(),
    download_url     = "git://github.com/T-002/pycast.git"
)