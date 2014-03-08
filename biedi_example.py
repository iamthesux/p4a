from sqp import *

# parse the mission files and create the data structures
mish3d = parse('mission.biedi')
mish2d = parse('sample2.sqm')

# we only want base parts for this example, this is a list of them
base_parts = [
	'Land_ConcreteBlock', 'Concrete_Wall_EP1', 'Land_BagFenceLong', 
	'MAP_BagFenceShort', 'MAP_BagFenceEnd', 'Land_prebehlavka'
]

# get all the top level classes whos object type is vehicle, and have an 
# Arguments subclass with a TYPE matching our desired base parts
parts3d = mish3d.filter(lambda x: x['objectType'] == "vehicle" and x('Arguments')['TYPE'] in base_parts)

# get the existing number of items in the missions vehicle
# class so we can name our items accordingly
if mish2d("Mission")("Vehicles"):
	c = mish2d("Mission")("Vehicles")["items"]
else:
	c = 0

# find the highest id in the Mission class
# if there are no ids assigned we want the first to end up zero
id = mish2d("Mission").hiid()
if id == None: id = -1


# for each part we create a new Item to put in the Vehicles class
# of our existsing mission
for part in parts3d:
	id+=1;
	# create the item class to which we attach all our data
	k = Klass('Item'+str(c))
	
	# biedi stores position as an array in string format.  pythons arrays
	# are identical so we can use eval to extract the array
	pos = eval(part('Arguments')['POSITION'])
	k['position'] = [pos[0], pos[2], pos[1]]
	
	if part('Arguments')['AZIMUT']:
		k['azimut'] = float(part('Arguments')['AZIMUT'])
	k['id'] = id
	k['side'] = "EMPTY"
	k['vehicle'] = part('Arguments')['TYPE']
	k['skill'] = 1.0
	k['init'] = "this setPos [%f, %f, %f];" % tuple(pos)
	
	# append the newly created class to the 2d mission data
	mish2d("Mission")("Vehicles")(k)
	
	# increment our item counter and set the number of items in our Vehicles class
	c+=1
	mish2d("Mission")("Vehicles")["items"] = c
	
# save the output to a file
open('mission.sqm', 'w').write(mish2d.to_string())

# k['azmt'] = 0.123
# k['pos'] = [1,2,3]

# root = Klass()
# root(k)

