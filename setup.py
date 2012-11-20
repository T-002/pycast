from distutils.core import setup

setup(
    name             = "pycast",
    version          = "v0.0.9-prealpha",
    author           = "Christian Schwarz",
    author_email     = "pixeldreck@gmail.com",
    packages         = ["pycast"],
    scripts          = ["bin"],
    url              = "http://code.google.com/p/py-cast/",
    license          = "LICENSE.txt",
    description      = "A Python Forecasting and Smoothing Library",
    long_description = open("README.txt").read(),
    install_requires = ["nose >= 1.2.1", "coverage >= 3.5.3"]
)