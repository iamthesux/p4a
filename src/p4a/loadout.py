import pprint

import cStringIO

_mode_flags = [
	'remove_weapons',
	'remove_items',
	'remove_link_items',
	'remove_uniform',
	'remove_vest',
	'remove_ruck',
	'remove_headgear',
	'remove_goggles',
	'remove_all',

	'clear_uniform',
	'clear_vest',
	'clear_ruck',
	'clear_all'
]
class LoadOut(object):
	def __init__(self, name=''):
		self._name = name
		self._flags = []

	@property
	def name(self):
		if self._name:
			return self._name
		else:
			return self.__class__.__name__
	@name.setter
	def name(self, name):
		self._name = name

	@property
	def flags(self):
		if self._name:
			return self._name
		else:
			return self.__class__.__name__
	@name.setter
	def flags(self, name):
		self._name = name

	def remove(self, slot):
		slot = 'remove_%s' % slot
		idx = _mode_flags.index(slot)
		if idx not in self._flags:
			self._flags.append(idx)

	def clear(self, slot):
		slot = 'clear_%s' % slot
		idx = _mode_flags.index(slot)
		if idx not in self._flags:
			self._flags.append(idx)
	def generate(self):
		res = []
		res.append(self._flags)
		
		for x in ['Primary','Secondary','HandGun']:
			wep = []
			if hasattr(self, x):
				atr = getattr(self, x)
				for i in ['weapon', 'supressor', 'rail', 'optic']:
					wep.append(getattr(atr, i, ''))
				wep.append(getattr(atr, 'mags', []))
			res.append(wep)
		
		for x in ['Uniform','Vest','Backpack']:
			pak = []
			if hasattr(self, x):
				atr = getattr(self, x)
				pak.append(getattr(atr, 'type', ''))
				if hasattr(atr, 'items'):
					pak.append(getattr(atr, 'items'))
			res.append(pak)
		if hasattr(self, 'items'):
			res.append(self.items)
		if hasattr(self, 'headgear'):
			res.append(self.headgear)
		return res
		
class Writer(object):
	def __init__(self, file=None):
		if isinstance(file, basestring):
			self.stream = open(file, 'wb')
		else:
			self.stream = cStringIO.StringIO()
		self.var_prefix = 'sux_lo_'
		
	def write(self, load):
		self.stream.write("%s%s = \n" % (self.var_prefix, load.name))
		pp = pprint.PrettyPrinter(indent=4, stream=self.stream)
		pp.pprint(load.generate())
		self.stream.write(";\n\n")
		return self.stream
		