import os, sys
sys.path.insert(0, os.path.abspath("../../src/"))
from p4a.formats.rap.text import Reader, Writer


rap = Reader('../testrap.cpp').read();

print rap('Mission')('Groups')('Item0')('Vehicles')('Item0')['position']