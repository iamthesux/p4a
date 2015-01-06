import os, sys
sys.path.insert(0, os.path.abspath("../src/"))
import re

from p4a.formats.rap import Klass
from p4a.formats.rap.binary import Reader as BinReader
from p4a.formats.rap.text import Writer

#Writer(sys.stdout).write(Reader('config2.bin').read())

import p4a.formats.pbo as pbo
file1 = 'sux_safehouse.pbo'
file2 = 'f:/armawork/pbo/structures_f.pbo'
pbo_reader = pbo.Reader(file2).read()

#print "len(pbof.header.entries)
#for e in pbof.header.filter(lambda x: re.search(r"config\.((bin)|(cpp))$", x.filename)):

e=next(ent for ent in pbo_reader.header.entries if re.search(r"config\.((bin)|(cpp))$", ent.filename))

template = "{file:<55}{size:>12}{pos:>12}"
print template.format(file='FILE', size='SIZE', pos='POSITION')
print template.format(file=e.filename, size=e.data_size, pos=e.pos)

pbo_reader.fh.seek(e.pos)
Writer(sys.stdout).write(BinReader(pbo_reader.fh).read())