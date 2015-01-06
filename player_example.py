from p4a.formats.rap.text import Reader, Writer
from p4a.formats.rap import Klass



teams = {}
teams['det5'] = dict(
	name = 'Det-5',
	side = 'WEST',
	groups = [
		[
			{
				'role': "Platoon Leader",
				'callsign': 'LANCER 1-6'
			}
		]
	],
)
base_pos = [4800,6,2260]


teams['mcru'] = dict(
	name = 'MCRU',
	side = 'WEST',

	groups = [
		# mcru admin
		[
			{
				'role': "OIC - Barnes B.L.",
				'callsign': 'RAIDER 1-6',
				'loadout': 'mcru_PL',
			},
			{
				'role': "XO - Kelly P.J.",
				'callsign': 'RAIDER 1-6',
				'loadout': 'mcru_PL',
			},
			{
				'role': "Gunnery Sergeant - McCarthy C.A.",
				'callsign': 'RAIDER 1-6',
				'loadout': 'mcru_PL',
			},			
			{
				'role': "Admin Chief - Presson R.M.",
				'callsign': 'RAIDER 1-6',
				'loadout': 'mcru_PL',
			},
		],
		# mcru hq
		[
			{
				'role': "Platoon Leader - Dorethy K.K.",
				'callsign': 'RAIDER 1-6',
				'loadout': 'mcru_PL',
			},
			{
				'role': "Platoon Sgt - Jones C.R.",
				'callsign': 'RAIDER 1-7',
				'loadout': 'mcru_PL',
			},
			{
				'role': "Platoon RTO",
				'callsign': 'RAIDER 1-6-R',
				'loadout': 'mcru_RTO',
			},
			{
				'role': "Platoon Medic",
				'callsign': 'RAIDER 1-6-M',
				'loadout': 'mcru_medic',
			},
		],
		# mcru squad 1
		[
			{
				'role': "Squad Leader",
				'callsign': 'RAIDER 1-1',
				'loadout': 'mcru_sl',
			},
			{
				'role': "Alpha - Team Leader",
				'callsign': 'RAIDER 1-1-A',
				'loadout': 'mcru_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'mcru_ar' },
			{ 'role': "Assistant AR", 'loadout': 'mcru_asst_ar' },
			{ 'role': "Rifleman", 'loadout': 'mcru_rifleman' },
			{
				'role': "Bravo - Team Leader",
				'callsign': 'RAIDER 1-1-B',
				'loadout': 'mcru_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'mcru_ar' },
			{ 'role': "Assistant AR", 'loadout': 'mcru_asst_ar' },
			{ 'role': "Rifleman", 'loadout': 'mcru_rifleman' },
			{
				'role': "Charlie - Team Leader",
				'callsign': 'RAIDER 1-1-C',
				'loadout': 'mcru_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'mcru_ar' },
			{ 'role': "Assistant AR", 'loadout': 'mcru_asst_ar' },
			{ 'role': "Rifleman", 'loadout': 'mcru_rifleman' },
		],
		# mcru squad 2
		[
			{
				'role': "Squad Leader",
				'callsign': 'RAIDER 1-2',
				'loadout': 'mcru_sl',
			},
			{
				'role': "Alpha - Team Leader",
				'callsign': 'RAIDER 1-2-A',
				'loadout': 'mcru_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'mcru_ar' },
			{ 'role': "Assistant AR", 'loadout': 'mcru_asst_ar' },
			{ 'role': "Rifleman", 'loadout': 'mcru_rifleman' },
			{
				'role': "Bravo - Team Leader",
				'callsign': 'RAIDER 1-2-B',
				'loadout': 'mcru_tl',
				'loadout': 'mcru_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'mcru_ar' },
			{ 'role': "Assistant AR", 'loadout': 'mcru_asst_ar' },
			{ 'role': "Rifleman", 'loadout': 'mcru_rifleman' },
			{
				'role': "Charlie - Team Leader",
				'callsign': 'RAIDER 1-2-C',
				'loadout': 'mcru_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'mcru_ar' },
			{ 'role': "Assistant AR", 'loadout': 'mcru_asst_ar' },
			{ 'role': "Rifleman", 'loadout': 'mcru_rifleman' },
		],
	],
)

teams['pubs'] = dict(
	name = 'pubics',
	side = 'WEST',
	groups = [
		# pubbie hq
		[
			{
				'role': "Platoon Leader",
				'callsign': 'LANCER 1-6',
				'loadout': 'pub_PL',
			},
			{
				'role': "Platoon Sgt",
				'callsign': 'LANCER 1-7',
				'loadout': 'pub_PL',
			},
			{
				'role': "Platoon RTO",
				'callsign': 'LANCER 1-6-R',
				'loadout': 'pub_RTO',
			},
			{
				'role': "Platoon Medic",
				'callsign': 'LANCER 1-6-M',
				'loadout': 'pub_medic',
			},
		],
		# pubbie squad 1
		[
			{
				'role': "Squad Leader",
				'callsign': 'LANCER 1-1',
				'loadout': 'pub_sl',
			},
			{
				'role': "Alpha - Team Leader",
				'callsign': 'LANCER 1-1-A',
				'loadout': 'pub_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'pub_ar' },
			{ 'role': "Grenadier", 'loadout': 'pub_grenadier' },
			{ 'role': "Rifleman", 'loadout': 'pub_rifleman' },
			{
				'role': "Alpha - Team Leader",
				'callsign': 'LANCER 1-1-B',
				'loadout': 'pub_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'pub_ar' },
			{ 'role': "Grenadier", 'loadout': 'pub_grenadier' },
			{ 'role': "Rifleman", 'loadout': 'pub_rifleman' },
		],
		# pubbie squad 2
		[
			{
				'role': "Squad Leader",
				'callsign': 'LANCER 1-1',
				'loadout': 'pub_sl',
			},
			{
				'role': "Alpha - Team Leader",
				'callsign': 'LANCER 1-1-A',
				'loadout': 'pub_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'pub_ar' },
			{ 'role': "Grenadier", 'loadout': 'pub_grenadier' },
			{ 'role': "Rifleman", 'loadout': 'pub_rifleman' },
			{
				'role': "Alpha - Team Leader",
				'callsign': 'LANCER 1-1-B',
				'loadout': 'pub_tl',
			},
			{ 'role': "Automatic Rifleman", 'loadout': 'pub_ar' },
			{ 'role': "Grenadier", 'loadout': 'pub_grenadier' },
			{ 'role': "Rifleman", 'loadout': 'pub_rifleman' },
		],
	],
)


mish = Reader('mission.sqm').read()
top_id = id_count = mish.hiid()
g_count = mish('Mission')('Groups')['items']

for team in ['pubs','16aa','mcru','sasr','160th','det5']:
	if team in teams:
		for grp in teams[team]['groups']:
			g = Klass('Item' + str(g_count))
			g['side'] = teams[team]['side']
			
			v = Klass('Vehicles')
			v_count = 0
			for unit in grp:
				u = Klass('Item' + str(v_count))
				u['position'] = [base_pos[0]+int((id_count-top_id)/10), base_pos[1], base_pos[2]+((id_count-top_id) % 10)]
				u['id'] = id_count
				u['side'] = teams[team]['side']
				u['vehicle'] = 'B_Soldier_F'
				
				if id_count == 0:
					u['player'] = 'PLAYER COMMANDER'
				else:
					u['player'] = 'PLAY CDG'
				u['skill'] = 0.60000002
				u['text'] = "%s_%d_%d" % (team, g_count, v_count)
				u['description'] = "%s // %s" % (teams[team]['name'], unit['role'])
				if 'callsign' in unit:
					u['description'] += " // %s" % (unit['callsign'])
				
				id_count += 1
				v_count += 1
				v['items'] = v_count
				v(u)
			g(v)
			g_count += 1
			mish('Mission')('Groups')['items'] = g_count
			mish('Mission')('Groups')(g)

Writer('../temp.Chernarus_Summer/mission.sqm').write(mish)

