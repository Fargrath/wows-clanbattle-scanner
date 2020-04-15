import re
from dataclasses import dataclass, field


#constants
PLAYERS_PER_TEAM = 7
DATE_PATTERN = '(\d{2})[/.-](\d{2})[/.-](\d{2}) (\d{2}):(\d{2})'	# %d.%m.%y %H:%M
RESULT_PATTERN = 'ClanBattlesTable__defeat__3Jl6w|ClanBattlesTable__victory__1DrFU'
MAP_PATTERN = 'Land des Feuers|Norden|Nördliche Gewässer|Zuflucht|Tränen der Wüste|Kampfzone Alpha|Weg des Kriegers|Dreizack'
PLAYER_PATTERN = '<div class="BattleTeamsList__nickname__1nkU_">(.+?)</div>'
SHIP_PATTERN = '<div class="BattleTeamsList__shipName__1QlOg">(.+?)</div>'

RESULT_TRANSLATION = {
	'ClanBattlesTable__defeat__3Jl6w': 'Defeat',
	'ClanBattlesTable__victory__1DrFU': 'Victory',
}

MAP_TRANSLATION = {
	'Land des Feuers' : 'Land of Fire',
	'Norden': 'North',
	'Nördliche Gewässer': 'Northern Waters',
	'Zuflucht': 'Haven',
	'Tränen der Wüste': 'Tears of the Desert',
	'Kampfzone Alpha': 'Crash Zone Alpha',
	'Weg des Kriegers': 'Warrior\'s Path',
	'Dreizack': 'Trident'
}

def csv_header(num_players = None):
	num_players = num_players or PLAYERS_PER_TEAM
	fields = ['DATE', 'TIME', 'RESULT', 'MAP']
	for i in range(num_players):
		fields.append(f'PLAYER {i+1}')
		fields.append(f'SHIP {i+1}')
	return ';'.join(fields)

def csv_row(battle, num_players = None):
	num_players = num_players or PLAYERS_PER_TEAM
	fields = [battle.date, battle.time, RESULT_TRANSLATION.get(battle.result, battle.result), MAP_TRANSLATION.get(battle.map, battle.map)]
	for i in range(num_players):
		fields.append(battle.players[i])
		fields.append(battle.ships[i])
	return ';'.join(fields)

@dataclass
class Battle:
	date: str
	time: str
	result: str
	map: str
	players: list = field(default_factory=list)
	ships: list = field(default_factory=list)
	
def load_data(file_name):
	with open(file_name, 'r', encoding='utf-8') as html_file:
		return html_file.read()

def search_regex(regex, html_data, group_index = 0):
	match = re.search(regex, html_data)
	if match:
		result = match.group(group_index)
		remaining_data = html_data[match.end():]
		return result, remaining_data
	return None, html_data
	
def scan_next_battle(html_data, num_players = None):
	num_players = num_players or PLAYERS_PER_TEAM
	
	while True:
		date_time, html_data = search_regex(DATE_PATTERN, html_data)
		if not date_time:
			return
		date,time = date_time.split()
		result, html_data = search_regex(RESULT_PATTERN, html_data)
		map, html_data = search_regex(MAP_PATTERN, html_data)
		b = Battle(date, time, result, map)
		for i in range(num_players):
			player, html_data = search_regex(PLAYER_PATTERN, html_data, group_index = 1)
			ship, html_data = search_regex(SHIP_PATTERN, html_data, group_index = 1)
			b.players.append(player)
			b.ships.append(ship)
		yield b
	
if __name__ == "__main__":
	import sys
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	
	data = load_data(input_file)
	with open(output_file, 'w+', encoding='utf-8') as out:
		out.write(csv_header())
		out.write('\n')
		for each_battle in scan_next_battle(data):
			out.write(csv_row(each_battle))
			out.write('\n')