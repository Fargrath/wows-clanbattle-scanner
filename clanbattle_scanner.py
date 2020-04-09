import re
from dataclasses import dataclass, field


#constants
PLAYERS_PER_TEAM = 4
DATE_PATTERN = '(\d{2})[/.-](\d{2})[/.-](\d{2}) (\d{2}):(\d{2})'	# %d.%m.%y %H:%M
RESULT_PATTERN = 'Niederlage|Sieg'
MAP_PATTERN = 'Dreizack|Zerklüftet|Gefahrenherd|Großes Rennen|Nördliche Gewässer'
PLAYER_PATTERN = '<div class="BattleTeamsList__nickname__1nkU_">(.+?)</div>'
SHIP_PATTERN = '<div class="BattleTeamsList__shipName__1QlOg">(.+?)</div>'

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
	if not num_players:
		num_players = PLAYERS_PER_TEAM
	
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
		for each_battle in scan_next_battle(data):
			out.write(str(each_battle))
			out.write('\n')