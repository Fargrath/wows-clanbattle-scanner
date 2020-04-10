import unittest
from clanbattle_scanner import *

class TestClanBattleScanner(unittest.TestCase):
	def test_csv_header(self):
		expected_header = 'DATE;TIME;RESULT;MAP;PLAYER 1;SHIP 1'
		self.assertEqual(csv_header(num_players = 1), expected_header)
		
	def test_csv_row(self):
		test_battle = Battle('04.04.20', '22:04', 'Sieg', 'Dreizack')
		test_battle.players.append('Player1')
		test_battle.ships.append('Ship1')
		expected_row = '04.04.20;22:04;Win;Trident;Player1;Ship1'
		self.assertEqual(csv_row(test_battle, num_players = 1), expected_row)
		
	def test_scan_next_battle(self):
		test_data = """
<div class="Table__value__2jmqw">04.04.20 22:04</div>
<div class="ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G">Sieg</div>
<div class="Table__value__2jmqw">Dreizack</div>
<div class="BattleTeamsList__nickname__1nkU_">Player1</div>
<div class="BattleTeamsList__shipName__1QlOg">Ship1</div>
"""
		expected_battle = Battle('04.04.20', '22:04', 'Sieg', 'Dreizack')
		expected_battle.players.append('Player1')
		expected_battle.ships.append('Ship1')
		for the_battle in scan_next_battle(test_data, num_players = 1):
			self.assertEqual(the_battle, expected_battle)

if __name__ == '__main__':
	unittest.main()