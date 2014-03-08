import shlex
import re
from collections import OrderedDict

_version=1

_kwp = re.compile(r'\W')
_uqp = re.compile(r'^"|"$')
_dqp = re.compile(r'""')

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
	elif re.search(r'-?^\d+\.\d+$', s):
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
		self._data = OrderedDict()
		self.name = _name
		self._hiid = None

	def __getattr__(self, att):
		"""
		These attributes are just helpfull accessors for the class data.  They
		do the following:
		
		klasses:  gets a list of all the sub classes
		keys: returns all the key/value keys. Not Implemented
		keys: returns both kvp and sub classes. Not Implemented
		"""
		if att == "klasses":
			return filter(lambda x: isinstance(x, Klass), self._data.keys())
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
			self._data[val] = val
		else:
			return self._data[Klass(val)]
			
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

	def hiid(self):
		"""
		This searches itself and all sub classes recursively for a key named
		id, then returns the highest number it finds as a value.
		"""
		c = None
		if 'id' in self._data and int(self._data['id']) > c:
			c = int(self._data['id'])
		for k in self.klasses:
			id = k.hiid()
			if  id > c:
				c = id
		return c

	def filter(self, f):
		"""
		A convenience method, calls the python filter function on all classes. Takes a function as an argument.
		"""
		return filter(f, self.klasses)
		
	def to_string(self, d=0):
		"""
		Converts the class to a properly formated and indented string.  Optionally takes
		a starting indent level as an argument.
		"""
		ret = ""
		if self.name:
			ret += ("\t"*(d-1)) + "class " + self.name + "\n" + ("\t"*(d-1)) + "{\n"
		for k,v in self._data.items():
			if isinstance(k, Klass):
				ret += k.to_string(d+1)
			else:
				ret += ("\t"*d)+ k
				if isinstance(v, list):
					ret += "[]="
					if isinstance(v[0], str) or len(v) > 3:
						ret +="\n" + ("\t"*d) + "{\n"
						tmp = ",\n" + ("\t"*(d+1))
						ret += ("\t"*(d+1)) + tmp.join(map(pvalue, v)) + "\n" + ("\t"*d) + "}"
					else:
						ret += "{" + ", ".join(map(pvalue,v)) + "}"
				else:
					ret += "=" + pvalue(v)
				ret += ";\n"
		if self.name:
			ret += ("\t"*(d-1)) + "};\n"

		return ret

def parse(file):
	"""
	Takes file name as an argument and returns a root Klass instance containing all the data.
	"""
	lex = shlex.shlex(open(file))
	lex.wordchars += '.'
	tokens = list(lex);

	ks = [Klass(),]
	bs = []
	kw = ""
	vw = ""
	va = []
	arval = False
	i = 0
	DEBUG=False
	while (i < len(tokens)):
		if DEBUG: print tokens[i]
		if (tokens[i] == "class" and tokens[i+1] != "="):
			if DEBUG: print "K"
			k = Klass(tokens[i+1])
			ks.append(k)
			bs.append(1)
			i+=3
		elif (tokens[i] == "{"):
			if DEBUG: print "KE"
			bs[-1]+=1
			i+=1
		elif (tokens[i] == "}"):
			
			bs[-1]-=1
			if bs[-1] == 0:
				if DEBUG: print "KL"
				k = ks.pop()
				ks[-1](k)
				bs.pop()
				i+=2;
			else:
				if DEBUG: print "KnL"
				i+=1
		elif not kw and not _kwp.search(tokens[i]):
			if DEBUG: print "kw"
			kw = tokens[i]
			if tokens[i+1] == "[":
				arval = True
				i+=4;
				va=[]
			else:
				arval=False
				vw=""
				i+=2
		elif tokens[i] == ";":
			if DEBUG: print "kve"
			if kw:
				if arval:
					ks[-1][kw] = va
				else:
					ks[-1][kw] = uq(value(vw))
				kw=""
			i+=1
		else:
			
			if arval:
				if tokens[i] != ",":
					if DEBUG: print "kva"
					va.append(uq(value(tokens[i])))
			else:
				if DEBUG: print "kvs"
				vw += tokens[i]
			i+=1
	return ks[0]

