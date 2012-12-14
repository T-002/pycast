from pycastobject import PyCastObject

def optimized(fn):
	def _optimized(self, *args, **kwargs):
		if self.optimization_enabled:
			class_name = self.__class__.__name__
			module = self.__module__.replace('pycast', 'pycastC')
			try:
				imported = __import__(module+"."+class_name, globals(), locals(), [fn.__name__])
				function = getattr(imported, fn.__name__)
				function(self, *args, **kwargs)
			except ImportError:
				print "[WARNING] Could not enable optimization for %s, %s" % (fn.__name__, self)
				fn(self, *args, **kwargs)
		else:
			fn(self, *args, **kwargs)
	return _optimized