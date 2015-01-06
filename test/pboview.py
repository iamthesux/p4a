import os, sys, wx
sys.path.insert(0, os.path.abspath("../src/"))

from p4a.formats.rap.binary import Reader as BinReader
from p4a.formats.pbo import Reader as PBOReader
#file = 'sux_safehouse.pbo'
file = 'f:/armawork/pbo/structures_f.pbo'

class MainWin(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(300,500))
		self.control = TreePBO(self,)# style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)
		self.Show(True)

class IconsPBO(wx.ImageList):
	def __init__(self, *args, **kwargs):
		super(IconsPBO, self).__init__(*args, **kwargs)
		self.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,wx.ART_OTHER,(16,16)))
		self.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,wx.ART_OTHER,(16,16)))

	

class TreePBO(wx.TreeCtrl):
	def __init__(self, *args, **kwargs):
		#super(TreePBO, self).__init__(*args, **kwargs)
		wx.TreeCtrl.__init__(self, *args, **kwargs)
		self.AssignImageList(IconsPBO(width=16, height=16))
		#self.SetItemComparator(FolderFileComparator())
		
		self.populate()
		#self.SortChildren(self.root)
	
	def OnCompareItems(self, item1, item2):
		if self.ItemHasChildren(item1) != self.ItemHasChildren(item2):
			if self.ItemHasChildren(item1):
				return -1
			else:
				return 1
		else:
			return cmp(self.GetItemText(item1),self.GetItemText(item2))

	def populate(self):
		self.reader = PBOReader(file).read()
		#if hasattr(self.reader.header.entries[0], 'strings'):
		self.root = self.AddRoot((file.split('\\'))[-1])
		for e in self.reader.header.entries:
			if e.filename:
				paths = e.filename.split('\\')
				
				base = self.root
				while len(paths) > 0:
					p = paths.pop(0)
					item = self.FindItem(base, p)
					if not item:
						item = self.AppendItem(base, p, 0)
						#self.SortChildren(item)
					base = item
				self.SetItemImage(item, 1)
				#self.SortChildren(item)
	def FindItem(self, item, label):
		(child, cookie) = self.GetFirstChild(item)
		while child.IsOk():
			if self.GetItemText(child).lower() == label.lower():
				return child
			(child, cookie) = self.GetNextChild(item, cookie)
		return None
app = wx.App(False)
frame = MainWin(None, file)
app.MainLoop()