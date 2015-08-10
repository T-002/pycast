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

import sys
sys.path.append('../../../')

import os
import sqlite3
import json
import itty

from pycast.methods.exponentialsmoothing import HoltWintersMethod
from pycast.optimization import GridSearch
from pycast.errors import SymmetricMeanAbsolutePercentageError as SMAPE
from pycast.common.timeseries import TimeSeries
from pycast.common.json_encoder import PycastEncoder

db = sqlite3.connect('energy.db')
MY_ROOT = os.path.join(os.path.dirname(__file__), 'static')

@itty.get('/energyData')
def energy_data():
    """
        Connects to the database and loads Readings for device 8.
    """
    cur = db.cursor().execute("""SELECT timestamp, current FROM Readings""")
    original = TimeSeries()
    original.initialize_from_sql_cursor(cur)
    original.normalize("day", fusionMethod = "sum")
    return itty.Response(json.dumps(original, cls=PycastEncoder), content_type='application/json')

@itty.post('/optimize')
def optimize(request):
    """
    Performs Holt Winters Parameter Optimization on the given post data.
    Expects the following values set in the post of the request:
        seasonLength - integer
        valuesToForecast - integer
        data - two dimensional array of [timestamp, value]
    """
    #Parse arguments
    seasonLength = int(request.POST.get('seasonLength', 6))
    valuesToForecast = int(request.POST.get('valuesToForecast', 0))
    data = json.loads(request.POST.get('data', []))

    original = TimeSeries.from_twodim_list(data)
    original.normalize("day") #due to bug in TimeSeries.apply
    original.set_timeformat("%d.%m")

    #optimize smoothing
    hwm = HoltWintersMethod(seasonLength = seasonLength, valuesToForecast = valuesToForecast)
    gridSearch = GridSearch(SMAPE)
    optimal_forecasting, error, optimal_params = gridSearch.optimize(original, [hwm])

    #perform smoothing
    smoothed = optimal_forecasting.execute(original)
    smoothed.set_timeformat("%d.%m")
    result = {  'params': optimal_params,
                'original': original,
                'smoothed': smoothed,
                'error': round(error.get_error(), 3)
                }
    return itty.Response(json.dumps(result, cls=PycastEncoder), content_type='application/json')

@itty.post('/holtWinters')
def holtWinters(request):
    """
    Performs Holt Winters Smoothing on the given post data.
    Expects the following values set in the post of the request:
        smoothingFactor - float
        trendSmoothingFactor - float
        seasonSmoothingFactor - float
        seasonLength - integer
        valuesToForecast - integer
        data - two dimensional array of [timestamp, value]
    """
    #Parse arguments
    smoothingFactor = float(request.POST.get('smoothingFactor', 0.2))
    trendSmoothingFactor = float(request.POST.get('trendSmoothingFactor', 0.3))
    seasonSmoothingFactor = float(request.POST.get('seasonSmoothingFactor', 0.4))
    seasonLength = int(request.POST.get('seasonLength', 6))
    valuesToForecast = int(request.POST.get('valuesToForecast', 0))
    data = json.loads(request.POST.get('data', []))

    #perform smoothing
    hwm = HoltWintersMethod(smoothingFactor = smoothingFactor,
                            trendSmoothingFactor = trendSmoothingFactor,
                            seasonSmoothingFactor =  seasonSmoothingFactor,
                            seasonLength = seasonLength,
                            valuesToForecast = valuesToForecast)
    original = TimeSeries.from_twodim_list(data)
    original.set_timeformat("%d.%m")
    smoothed = hwm.execute(original)
    smoothed.set_timeformat("%d.%m")

    error = SMAPE()
    error.initialize(original, smoothed)

    #process the result
    result = {  'original': original,
                'smoothed': smoothed,
                'error': round(error.get_error(), 3)
            }
    return itty.Response(json.dumps(result, cls=PycastEncoder), content_type='application/json')

@itty.get('/')
def index(request):
    return itty.serve_static_file(request, 'index.html', root=os.path.join(os.path.dirname(__file__), './'))

@itty.get('/static/(?P<filename>.+)')
def serve_static(request, filename):
    return itty.serve_static_file(request, filename, root=MY_ROOT)

itty.run_itty()