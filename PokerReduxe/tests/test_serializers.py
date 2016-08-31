import unittest
import json

from serializers import TableEncoder

from gamelogic.player import Player
from gamelogic.table import Table
from gamelogic.pot import Pot


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

    def test_class_to_json(self):
        """ Can we convert our Python Class to json string? """
        result = json.dumps(self.table, cls=TableEncoder,  check_circular=False)
        self.assertTrue(type(result), str())

if __name__ == '__main__':
    unittest.main()
