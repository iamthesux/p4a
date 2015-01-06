from p4a.formats.rap import Klass
from p4a.formats.rap.text import Reader, Writer

mish3d = Reader('mish.biedi').read()
mish2d = Reader('../rup.Zargabad/mission.sqm').read()


parts3d = mish3d.filter(lambda x: x['objectType'] == "vehicle")

# get the existing number of items in the missions vehicle
# class so we can name our items accordingly
if "Vehicles" in mish2d("Mission"):
	c = mish2d("Mission")("Vehicles")["items"]
else:
	mish2d("Mission")(Klass("Vehicles"))
	c = 0

# find the highest id in the Mission class
# if there are no ids assigned we want the first to end up zero
id = mish2d("Mission").hiid()
if id == None: id = -1
acc = tkc = 0
# for each part we create a new Item to put in the Vehicles class
# of our existsing mission
for part in parts3d:
	id+=1;
	# create the item class to which we attach all our data
	k = Klass('Item'+str(c))
	
	pos = eval(part('Arguments')['POSITION'])
	while len(pos) < 3: pos.append(0)

	k['position'] = [pos[0], pos[2], pos[1]]

	if part('Arguments')['AZIMUT']:
		k['azimut'] = float(part('Arguments')['AZIMUT'])
	
	k['id'] = id
	k['side'] = "EMPTY"
	k['vehicle'] = part('Arguments')['TYPE']
	k['skill'] = 1.0
	k['init'] = "this setPos [%f, %f, %f];" % tuple(pos)
	if part('Arguments')['NAME']:
		k['text'] = part('Arguments')['NAME']
	if part('Arguments')['INIT']:
		k['init'] += part('Arguments')['INIT']
	
	if part('Arguments')['TYPE'] == 'rhs_btr60_msv':
		tkc+=1
		k['text'] = "tech_spawn%d" % tkc
	elif part('Arguments')['TYPE'] == 'rup_ammo_box':
		k['text'] = "rup_ammo_crate_%d" % (acc+2)
		acc+=1
	elif part('Arguments')['TYPE'] == 'T34_TK_EP1':
		k['text'] = part('Arguments')['NAME']
	
	# append the newly created class to the 2d mission data
	mish2d("Mission")("Vehicles")(k)
	
	# increment our item counter and set the number of items in our Vehicles class
	c+=1
	mish2d("Mission")("Vehicles")["items"] = c


mish2d("Mission")("Intel")["briefingName"] = "Rainbow Unicorn Princess";

Writer('mission.sqm').write(mish2d)


