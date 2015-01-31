import re
from StringIO import StringIO
_kwp = re.compile(r'\W')
_uqp = re.compile(r'^"|"$')
_dqp = re.compile(r'""')

def israP(fh):
	s = fh.read(4)
	val = False
	if s == "\0raP":
		val = True
	fh.seek(-4, 1)
	return val

def uq(s):
	"""
	Removes and leading and ending quotes and unescapes
	quotes inside the string
	"""
	if isinstance(s, str):
		s = re.sub(_uqp, '', s)
		s = re.sub(_dqp, '"', s)
	return s
	
def qq(s):
	"""
	Surrounds a string with quotes and escapes
	quotes inside the string
	"""
	s = re.sub(r'"', '""', s)
	s = '"' + s + '"'
	return s

def value(s):
	"""
	Attempts to marshall integers, decimals and strings into 
	their respective types.
	"""
	s = str(s)
	if re.search(r'^-?\d+$', s):
		return int(s)
	elif re.search(r'^-?\d+\.\d+$', s):
		return float(s)
	else:
		return uq(s)

def pvalue(val):
	"""
	Formats a value for printing.  Strings get escaped and quoted, numbers
	are converted to string.
	"""
	if isinstance(val, str):
		return qq(val)
	else: 
		return str(val)

def armatch(arr, string):
	for var in arr:
		if isinstance(var, list):
			return armatch(var, string)
		else:
			if string in str(var):
				return True
	return False
class Klass:
	"""
	A class that represents the base data structure.  Like an Arma class, it 
	contains both key value pairs as well as sub classes.  A nameless root
	level Klass represents a document.  All of your datums are belong to it.
	"""
	

	def __init__(self, _name=""):
		"""
		Creates an new Klass instance.  If name is empty, the class is considered
		root level and when converted to string, it only writes its key/value pairs
		and subclasses.  In other words, to create a class that represents your base
		document, call init with no args
		"""
		from collections import OrderedDict
		self._data = OrderedDict()
		self.name = _name
		self._hiid = None
		self.parent = None

	def __getattr__(self, att):
		"""
		These attributes are just helpfull accessors for the class data.  They
		do the following:
		
		klasses:  gets a list of all the sub classes
		inherits: returns a classes parent if assigned
		keys: returns all the key/value keys. Not Implemented
		keys: returns both kvp and sub classes. Not Implemented
		"""
		if att == "klasses":
			return filter(lambda x: isinstance(x, Klass), self._data.keys())
		elif att in ['inherits', 'extern', 'delete']:
			return False
		elif att == "parents":
			parents = []
			p = self.parent
			while p:
				parents.append(p.name)
				p = p.parent
		else:
			raise AttributeError

	def __hash__(self):
		return hash(self.name)
	def __eq__(self, val):
		if self.__hash__() == val.__hash__():
			return True
		return False

	def __call__(self, val=None):
		"""
		Call or (), is overidden to provide features similar to a dict except it
		is used for sub classes.  If no args are provided it returns its sub 
		classes.  
		
		If passed a Klass instance, the Klass is added as a sub class. This 
		will overwrite any sub class already existing with the same name.
		
		If passed a the name of a class as a string, it will return the sub 
		class with that name, or None if none exists.
		"""
		if val == None:
			return self.klasses
		if isinstance(val, Klass):
			if val in self._data:
				del self._data[val]
			val.parent = self
			self._data[val] = val
		else:
			return self._data[Klass(val)]

	def __contains__(self, val):
		return Klass(val) in self._data

	def __getitem__(self, idx):
		"""
		Get item and set item provide access to the key/value data of a
		class.
		"""
		try:
			return self._data[idx]
		except KeyError:
			return None
	def __setitem__(self, idx, item=None):
		self._data[idx] = item

	def match(self, string):
		if self.name == string:
			return True
		for key, val in self._data.iteritems():
			if isinstance(key, Klass):
				if key.match(string):
					return True
			else:
				if string in key:
					return True
				if isinstance(val, list):
					if armatch(val, string):
						return True
				else:
					if string in str(val):
						return True
		return False
					
	def hiid(self):
		"""
		This searches itself and all sub classes recursively for a key named
		id, then returns the highest number it finds as a value.
		
		TODO: obsolete this use nextid
		"""
		c = None
		if 'id' in self._data and int(self._data['id']) > c:
			c = int(self._data['id'])
		for k in self.klasses:
			id = k.hiid()
			if  id > c:
				c = id
		return c
	
	def nextid(self):
		"""
		This searches itself and all sub classes recursively for a key named
		id, then returns the highest number it finds as a value.
		"""
		c = 0
		if 'id' in self._data and int(self._data['id']) > c:
			c = int(self._data['id'])
		for k in self.klasses:
			id = k.hiid()
			if  id > c:
				c = id
		return c+1
	
	def filter(self, f):
		"""
		A convenience method, calls the python filter function on all classes. Takes a function as an argument.
		"""
		return filter(f, self.klasses)

