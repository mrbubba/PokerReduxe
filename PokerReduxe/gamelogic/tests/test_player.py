import unittest

from player import Player
from table import Table
from pot import Pot
import app


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("player1", 100)
        self.table = Table(6, 1, 2, [50, 100])
        self.table.join(1, self.player, 100)
        pot1 = Pot([self.player], 100)
        pot2 = Pot([self.player], 100)
        self.table.pots = [pot1, pot2]

    def test_bet(self):
        """Does bet subtract from stack and add to equity"""
        self.player.bet(20)
        self.assertEqual(80, self.player.stack)
        self.assertEqual(20, self.player.equity)

    def test_bet_negative_int_fails(self):
        """Do we throw an error when bet is a negative number?"""
        with self.assertRaises(Exception) as context:
            self.player.bet(-50)
        self.assertIn("Bets can not be negative", str(context.exception))

    def test_call(self):
        """Can we insure that the bettor at least matches the minimum bet??"""


if __name__ == '__main__':
    unittest.main()
