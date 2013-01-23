import json

from pycastobject import PyCastObject
class PycastEncoder(json.JSONEncoder, PyCastObject):
    def default(self, obj):

		# Cannot use the to_json method, because it returns a string rather
		# than a serializable list.
        return obj.to_twodim_list()