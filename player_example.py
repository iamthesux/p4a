from sqp import *

mish = parse('test.sqm')
for grp in mish('Mission')('Groups').filter(lambda g: g['side'] == "WEST"):
	print grp.name
	for plyr in grp('Vehicles')():
		if not plyr['player']:
			plyr['player'] = "PLAY CDG"
		plyr['init'] = 'nul = [] execVM "playerInit.sqf";'
		
open('output.sqm', 'w').write(mish.to_string())