import pprint
import cStringIO

from .formats.rap import Klass

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
	def __init__(self, **kwargs):
		self._flags = []
		if 'prefix' in kwargs:
			self._prefix = kwargs.pop('prefix', '')
		if 'name' in kwargs:
			self._name = kwargs.pop('name', '')
	@property
	def name(self):
		if hasattr(self, '_name'):
			return self._name
		else:
			return self.__class__.__name__
	@name.setter
	def name(self, name):
		self._name = name

	
	@property
	def base(self):
		if hasattr(self, '_base'):
			return self._base
		else:
			return ''
	@base.setter
	def base(self, base):
		self._base = base

	@property
	def prefix(self):
		if hasattr(self, '_prefix'):
			return self._prefix
		else:
			return ''
	@prefix.setter
	def prefix(self, prefix):
		self._prefix = prefix

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
				for i in ['weapon', 'suppressor', 'rail', 'optic']:
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
	def generate_config(self):
		k = Klass(self.prefix + self.name)
		k.inherits = self.base
		
		k['scope'] = 2
	def write(self):
		f = open(self.name + '.sqf', 'wb')
		f.write(str(self.generate()) + ';')

class Crate(LoadOut):
	class NoWrite: pass
	def __init__(self, **kwargs):
		super(Crate, self).__init__(**kwargs)
		if not self.base:
			self.base = 'Box_NATO_AmmoOrd_F'
	@property
	def title(self):
		if hasattr(self, '_title'):
			return self._title
		else:
			return ''
	@title.setter
	def title(self, title):
		self._title = title

	@property
	def side(self):
		if hasattr(self, '_side'):
			return self._side
		else:
			return ''
	@side.setter
	def side(self, side):
		self._side = side




	def generate(self):
		res = []
		for x in ['weapons','magazines','backpacks','items']:
			if hasattr(self, x):
				res.append(getattr(self, x))
		return res
	def generate_config(self):
		k = Klass(self.prefix + self.name)
		k.inherits = self.base
		k['scope'] = 2
		
		k['displayName'] = self.title
		k['maximumLoad'] = 9999999
		k['transportMaxMagazines'] = 9999999
		k['transportMaxMagazines'] = 9999999
		k['transportMaxBackpacks'] = 9999999
		
		for type in ['weapons','magazines','backpacks','items']:
			tk = Klass("Transport%s" % type.title())
			if hasattr(self, type):
				for item in getattr(self, type):
					wk = Klass("_xx_%s" % item[0])
					if type == 'items':
						wk['name'] = item[0]
					else:
						wk[type[:-1]] = item[0]
					wk['count'] = item[1]
					tk(wk)
			k(tk)
		return k
