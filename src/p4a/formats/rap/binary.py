from struct import unpack, pack
from . import Klass
DEBUG = False
def asciz(fh):
	s = ''
	c = fh.read(1)
	while c != chr(0):
		s+=c
		c = fh.read(1)
	return s

def cint(fh):
	num=0
	b = fh.read(1)
	n = ord(b)
	if n & 0x80:
		for i in range(4):
			b = ord(fh.read(1))
			n += (b - 1) * 0x80
			if not(b & 0x80):
				break
	return n	
	#return unpack('<I', num)[0]
	
def rint(fh):
	return unpack('<I', fh.read(4))[0]
def rfloat(fh):
	return unpack('<f', fh.read(4))[0]

class Variable(str):
	def __init__(self, fh):
		self = asciz(fh)

class Entry(object):
	def parse(self, fh):
		self.name = asciz(fh)

class Class(Entry):

	def parse(self, fh):
		super(Class, self).parse(fh)
		self.klass = Klass(self.name)
		pos = rint(fh)
		
		#print "%(n)s -> %(p)d" % dict(n=self.name, p=pos)
		curpos = fh.tell()
		fh.seek(fh.start + pos)
		self.klass.inherits = asciz(fh)
		num = cint(fh)
		if DEBUG:
			print "CLASS: %(n)s -> %(p)d[%(num)d]" % dict(n=self.name, p=pos, num=num)
		for i in range(num):
			e = ParseEntry(fh)
			if type(e) is Class:
				self.klass(e.klass)
			elif type(e) is Extern:
				self.klass(e.klass)
			elif type(e) in [Value, Array]:
				self.klass[e.name] = e.value
		fh.seek(curpos)

class Extern(Entry):
	def parse(self, fh):
		super(Extern, self).parse(fh)
		self.klass = Klass(self.name)
		self.klass.extern = True
		if DEBUG: print "EXTERN: %(n)s" % dict(n=self.name)
		
ValueTypes = [asciz, rfloat, rint, rint, Variable]

class Value(Entry):
	def parse(self, fh):
		t = ord(fh.read(1))
		super(Value, self).parse(fh)
		self.value = ValueTypes[t](fh)
		
		if DEBUG: print ("VALUE:%(t)s:%(n)s = %(val)s" % 
			dict(n=self.name,val=str(self.value),t=ValueTypes[t].__name__))

class Array(Entry):
	def __init__(self):
		self.value = []
	def parse(self, fh):
		super(Array, self).parse(fh)
		num = cint(fh)
		if DEBUG: print "ARRAY: %(n)s[%(num)d]" % dict(n=self.name,num=num)
		for i in range(num):
			self.value.append(ParseEntry(fh, True))

class Delete(Entry):
	def parse(self, fh):
		super(Delete, self).parse(fh)
		self.klass = Klass(self.name)
		self.klass.delete = True
		if DEBUG: print '%s:%s' % (self.klass.delete,self.name)
		#raise NotImplementedError

class NestedArray(list):
	def __init__(self, fh):
		super(NestedArray, self).__init__()
		num = cint(fh)
		for i in range(num):
			self.append(ParseEntry(fh, True))
			
class BaseClass(Entry):
	def __init__(self):
		self.klass = Klass()
	def parse(self, fh):
		super(BaseClass, self).parse(fh)
		num = cint(fh)
		for i in range(num):
			e = ParseEntry(fh)
			if type(e) in [Class, Extern, Delete]:
				self.klass(e.klass)
			elif type(e) in [Value, Array]:
				self.klass[e.name] = e.value
		
Types = [Class,Value,Array,Extern,Delete]
ArrayTypes = [asciz,rfloat,rint,NestedArray,Variable]



def ParseEntry(fh,arr=False):
	t = ord(fh.read(1))
	
	if arr:
		val = ArrayTypes[t](fh)
		return val
	else:
		e = Types[t]()
		e.parse(fh)
	return e
class streamF(object):
	def __init__(self, f):
		self._fh = f
		self.start = f.tell()
		
	def __getattr__(self, attr):
		if attr in self.__dict__:
			return getattr(self, attr)
		return getattr(self._fh, attr)

class Reader:
	def __init__(self, f, pos=0):
		if type(f) in [str, unicode]:
			fh = open(f, 'rb')
			fh.seek(pos)
			self.fh = streamF(fh)
		else:
			self.fh = streamF(f)
	def read(self):
		s = self.fh.read(4)
		if s != "\0raP":	
			return None
		
		base = BaseClass()
		self.fh.seek(12,1)
		base.parse(self.fh)
		return base.klass
