import json
from timeseries import TimeSeries

class PycastEncoder(json.JSONEncoder):
    def default(self, obj):

		# Cannot use the to_json method, because it returns a string rather
		# than a serializable list.
        return obj.to_twodim_list()