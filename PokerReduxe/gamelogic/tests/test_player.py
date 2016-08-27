import unittest

from player import Player
from table import Table
from pot import Pot
import app


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("player1", 100)
        self.player2 = Player("player2", 100)
        self.player.action = True
        self.table = Table(6, 1, 2, [50, 100])
        self.table.join(1, self.player, 100)
        self.table.join(2, self.player2, 100)
        pot1 = Pot([self.player, self.player2], 100)
        pot2 = Pot([self.player, self.player2], 100)
        self.table.pots = [pot1, pot2]

    def test_bet(self):
        """Does bet subtract from stack and add to equity"""
        self.player.bet(20)
        self.assertEqual(80, self.player.stack)
        self.assertEqual(20, self.player.equity)
        self.assertFalse(self.player.action)

    def test_bet_negative_int_fails(self):
        """Do we throw an error when bet is a negative number?"""
        with self.assertRaises(Exception) as context:
            self.player.bet(-50)
        self.assertIn("Bets can not be negative", str(context.exception))

    def test_call(self):
        """Can we ensure that the bettor at least matches the minimum bet??"""
        self.table.current_bet = 20
        with self.assertRaises(Exception) as context:
            self.player.bet(10)
        self.assertIn("Must match the current bet", str(context.exception))

    def test_all_in(self):
        """ Can a player go all in, even for less than min bet? """
        self.table.current_bet = 20
        self.player.stack = 10
        self.player.bet(10)
        self.assertTrue(self.player.equity == 10)
        self.assertTrue(self.table.pots[-1].side_pots[0] == 10)

    def test_min_raise(self):
        """ Can we ensure that players cant raise less than the min? """
        with self.assertRaises(Exception) as context:
            self.player.bet(1)
        self.assertIn("Minimum raise is 2", str(context.exception))

    def test_max_bet_is_all_in(self):
        """ Can we ensure that players cant bet/raise more than their stack? """
        with self.assertRaises(Exception) as context:
            self.player.bet(200)
        self.assertIn("You can only bet what you have on the table!!", str(context.exception))

    def test_bet_increment_adjusted(self):
        """ Can we set/adjust the bet increment appropriately? """
        self.player.bet(50)
        self.assertEqual(self.table.bet_increment, 50)

    def test_call_action(self):
        """ Can we call action time appropriately """
        pass

if __name__ == '__main__':
    unittest.main()
