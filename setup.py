from distutils.core import setup

setup(
    name             = "pycast",
    version          = "0.0.1-prealpha",
    author           = "Christian S",
    author_email     = "pixeldreck@gmail.com",
    packages         = ["pycast"],
    scripts          = ["bin"],
    url              = "http://code.google.com/p/py-cast/",
    license          = "LICENSE.txt",
    description      = "A Python Forecasting and Smoothing Library",
    long_description = open("README.txt").read(),
    install_requires = []
#        "Django >= 1.1.1",
#        "caldav == 0.1.4",
)