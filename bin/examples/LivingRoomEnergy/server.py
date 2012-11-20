from itty import *
import json, sqlite3
sys.path.append('../../../')
from pycast.methods.exponentialsmoothing import HoltWintersMethod 
from pycast.common.timeseries import TimeSeries

db = sqlite3.connect('energy.db')
MY_ROOT = os.path.join(os.path.dirname(__file__), 'static')

@get('/')
def index(request):
	return serve_static_file(request, 'index.html', root=os.path.join(os.path.dirname(__file__), './'))

@get('/sampleData')
def sample_data(request):
	result = [[1350029449.14, 0.988454545454551], [1350115849.14, 0.7318750000000174], [1350202249.14, 1.1735972850678742]]
	return json.dumps(result)

@get('/energyData')
def energy_data(request):
	"""
		Connects to the database and loads Readings for device 8.
	"""
	cur = db.cursor().execute("""SELECT timestamp, current FROM Readings WHERE deviceId = 8""")
	original = TimeSeries()
	original.initialize_from_sql_cursor(cur)
	original.normalize("day")
	result = [entry for entry in original]
	return Response(json.dumps(result), content_type='application/json')

@post('/holtWinters')
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
	smoothed = hwm.execute(original)
	
	#process the result	
	result = {	'x': zip(*original)[0], #extracts the first dimension of the two dimensional list
				'original': [entry for entry in original],
				'smoothed': [entry for entry in smoothed]}
	return Response(json.dumps(result), content_type='application/json')

@get('/static/(?P<filename>.+)')
def serve_static(request, filename):
	return serve_static_file(request, filename, root=MY_ROOT)

run_itty()