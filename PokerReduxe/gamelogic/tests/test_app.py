import unittest

from table import Table
from player import Player
import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("player1")
        self.player2 = Player("player2")
        self.player3 = Player("player3")
        self.player4 = Player("player4")
        self.player5 = Player("player5")
        self.player6 = Player("player6")

        self.table = Table(6, 1, 2, [50, 100])

        self.table.join(1, self.player1, 100)
        self.table.join(2, self.player2, 100)
        self.table.join(3, self.player3, 100)
        self.table.join(4, self.player4, 100)
        self.table.join(5, self.player5, 100)
        self.table.join(6, self.player6, 100)

    def test_get_active_players(self):
        """ Can we grab a list of active players? """
        six_players = app.get_active_players(self.table)
        self.player1.active = False
        five_players = app.get_active_players(self.table)
        self.assertEqual(6, len(six_players))
        self.assertEqual(5, len(five_players))

    def test_reset_player_order(self):
        """ Can we randomly set the button? """
        call1 = app.reset_player_order(self.table)[:]
        call2 = app.reset_player_order(self.table)[:]
        call3 = app.reset_player_order(self.table)[:]
        call4 = app.reset_player_order(self.table)[:]
        call5 = app.reset_player_order(self.table)[:]

        self.assertFalse(call1 == call2 == call3 == call4 == call5)

if __name__ == '__main__':
    unittest.main()
