from struct import unpack
import sys, os, re

bzero = chr(0)
DEBUG = False
# class TreePBO(object):
	# def __init__(self):
		# self.data = []
		# self.root = NodePBO()
	# def add_path(self, path):
		# paths = path.split('\\')
		#val = paths.pop(-1)
		# spot = self.data
		# while len(paths) > 1:
			# try:
				# spot = spot[spot.index(p)]
			# except ValueError:
				# spot.append([p])
		
# class NodePBO:
	# def __init__(self, name):
		# self.name = name
		# self.nodes = []
		# self.items = []
	# def has
class Entry:
	def __init__(self):
		self.special = False
		self.filename = ''

	@staticmethod
	def parse(fh, header=False):
		e = Entry()
		c = fh.read(1)
		if c == bzero:
			e.special = True
			e.strings = []
		while c != bzero:
			e.filename += c
			c = fh.read(1)
			
		for x in ['packing_method', 'original_size', 'reserved', 'timestamp', 'data_size']:
			setattr(e, x, unpack('<I', fh.read(4))[0])
		
		if e.special and bool(e):
			c = fh.read(1)
			if c != bzero:
				while c != bzero:
					s=''
					while c != bzero:
						s += c
						c = fh.read(1)
					e.strings.append(s)
					c = fh.read(1)
		return e
	def __nonzero__(self):
		return (bool(self.filename)
			or self.packing_method
			or self.original_size
			or self.reserved
			or self.timestamp
			or self.data_size
			or len(self.strings))

class Header:
	def __init__(self):
		self.entries = []
	def filter(self, func):
		return filter(func, self.entries)

	@staticmethod
	def parse(fh):
		h = Header()
		fh.seek(0)
		e = Entry.parse(fh)
		while e:
			h.entries.append(e)
			e = Entry.parse(fh)
		h.size = fh.tell()
		return h

class Reader:
	def __init__(self, f):
		if type(f) in [str, unicode]:
			self.fh = open(f, "rb")
		else:
			self.fh = f
	def read(self):
		self.header = Header.parse(self.fh)
		c = self.header.size
		for ent in self.header.entries:
			ent.pos = c
			c += ent.data_size
		
		return self
