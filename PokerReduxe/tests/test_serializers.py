import unittest

from PokerReduxe.gamelogic.player import Player
from PokerReduxe.gamelogic.table import Table
from PokerReduxe.gamelogic.pot import Pot


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("player1", 100)
        self.player2 = Player("player2", 100)
        self.player.action = True
        self.table = Table("Table", 6, 1, 2, [50, 100])
        self.table.join(1, self.player, 100)
        self.table.join(2, self.player2, 100)
        pot1 = Pot([self.player, self.player2], 100)
        pot2 = Pot([self.player, self.player2], 100)
        self.table.pots = [pot1, pot2]


if __name__ == '__main__':
    unittest.main()
