import unittest
from clanbattle_scanner import *

class TestClanBattleScanner(unittest.TestCase):

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