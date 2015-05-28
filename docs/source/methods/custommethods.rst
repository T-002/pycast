.. index

Custom Methods
==============
Custom smoothing and forecasting methods must either inherit from `pycast.methods.BaseMethod` or `pycast.methods.BaseForecastingMethod` and implement the following functions:


  - `__init__(self, *args, **kwargs)`
  - `execute(self, timeSeries)`
  - `get_parameter_intervals(self)`

Code to start with
------------------
To implement your custom method, it is recommended to start with the following example::

    #!/usr/bin/env python
    # -*- coding: UTF-8 -*-
    
    #Copyright (c) 2012-2015 Christian Schwarz
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
    
    from pycast.methods import BaseMethod
    from pycast.common.timeseries import TimeSeries
    
    class CustomSmoothingMethod(BaseMethod):
    ## Alternative:
    ### class CustomForecastingMethod(BaseMethod):
    """This is your custom Method""" 
 
        def __init__(self, *args, **kwargs): 
            """Initializes the BaseMethod. 

            :param List args:    Arguments that are required for initialization.
            :param Dictionary hasToBeSorted:    Keyword arguments that are required for initialization.
            """ 
            super(BaseMethod, self).__init__(requiredParameters, hasToBeSorted, hasToBeNormalized)  

            ## YOUR CUSTOM CODE HERE
 
        def _get_parameter_intervals(self): 
            """Returns the intervals for the methods parameter. 

            Only parameters with defined intervals can be used for optimization!

            :return:    Returns a dictionary containing the parameter intervals, using the parameter 
                name as key, while the value hast the following format: 

                [minValue, maxValue, minIntervalClosed, maxIntervalClosed] 

                    - minValue
                        Minimal value for the parameter 

                    - maxValue 
                        Maximal value for the parameter 

                    - minIntervalClosed 
                        :py:const:`True`, if minValue represents a valid value for the parameter.
                        :py:const:`False` otherwise. 

                    - maxIntervalClosed: 
                        :py:const:`True`, if maxValue represents a valid value for the parameter. 
                        :py:const:`False` otherwise. 

            :rtype:     Dictionary 
            """ 
            parameterIntervals = {} 
    
            ## YOUR METHOD SPECIFIC CODE HERE! 
    
            return parameterIntervals 

        def execute(self, timeSeries): 
        """Executes the BaseMethod on a given TimeSeries object. 

        :param TimeSeries timeSeries: TimeSeries object that fullfills all requirements (normalization, sortOrder). 

        :return:    Returns a TimeSeries object containing the smoothed/forecasted values. 
        :rtype:     TimeSeries 

        :raise:    Raises a :py:exc:`NotImplementedError` if the child class does not overwrite this function. 
        """
        ## YOUR METHOD SPECIFIC CODE HERE! 