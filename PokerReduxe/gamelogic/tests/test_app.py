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

        # Set player order; happy path
        for k,v in self.table.seats.items():
            self.table.player_order.append(v)

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

    def test_move_button(self):
        """ Can we properly increment through the player order? """
        expected = self.table.player_order[:]
        x = expected.pop(0)
        expected.append(x)
        app.move_button(self.table)
        self.assertEqual(expected, self.table.player_order)

    def test_remove_inactive_from_hand(self):
        """ Can we remove an inactive player from a hand """
        self.player4.active = False
        app.move_button(self.table)
        self.assertEqual(len(self.table.player_order), 5)

    def test_add_player_to_hand(self):
        """ Can we add a new player to hand appropriately """
        expected = self.table.player_order[:]
        x = expected.pop(0)
        expected.append(x)
        x = expected.pop(0)
        expected.append(x)
        self.player4.active = False
        app.move_button(self.table)
        self.player4.active = True
        app.move_button(self.table)
        self.assertEqual(len(self.table.player_order), 6)
        self.assertEqual(expected, self.table.player_order)

    def test_bb_mia(self):
        """ Can we prepend sb position to None if bb goes mia """
        self.table.player_order[1].active = False
        app.move_button(self.table)
        self.assertEqual(self.table.player_order[0], None)
        expected = self.table.player_order[:]
        expected.pop(0)
        app.move_button(self.table)
        self.assertEqual(expected, self.table.player_order)

    def test_set_missed_bb(self):
        """ Can we set missed bb to True """
        self.player3.active = False
        app.move_button(self.table)
        self.assertTrue(self.player3.missed_bb)

    def test_set_missed_sb(self):
        """ Can we set missed sb to True """
        self.player2.active = False
        app.move_button(self.table)
        self.assertTrue(self.player2.missed_sb)

if __name__ == '__main__':
    unittest.main()
