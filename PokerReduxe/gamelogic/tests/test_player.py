import unittest


from PokerReduxe.gamelogic.table import Table
from PokerReduxe.gamelogic.pot import Pot


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.table = Table("Table", 6, 1, 2, [50, 100])
        self.table.join(1, 'player1', 100)
        self.table.join(2, 'player2', 100)
        self.table.join(3, 'player3', 100)
        self.table.seats[1].action = True
        pot1 = Pot([self.table.seats[1], self.table.seats[2], self.table.seats[3]], 100)
        pot2 = Pot([self.table.seats[1], self.table.seats[2], self.table.seats[3]], 100)
        self.table.pots = [pot1, pot2]

    def test_bet(self):
        """Does bet subtract from stack and add to equity"""
        self.table.seats[1].bet(20)
        self.assertEqual(80, self.table.seats[1].stack)
        self.assertEqual(20, self.table.seats[1].equity)
        self.assertFalse(self.table.seats[1].action)

    def test_bet_negative_int_fails(self):
        """Do we throw an error when bet is a negative number?"""
        with self.assertRaises(Exception) as context:
            self.table.seats[1].bet(-50)
        self.assertIn("Bets can not be negative", str(context.exception))

    def test_call(self):
        """Can we ensure that the bettor at least matches the minimum bet??"""
        self.table.current_bet = 20
        with self.assertRaises(Exception) as context:
            self.table.seats[1].bet(10)
        self.assertIn("Must match the current bet", str(context.exception))

    def test_all_in(self):
        """ Can a player go all in, even for less than min bet? """
        self.table.current_bet = 20
        self.table.seats[1].stack = 10
        self.table.seats[1].bet(10)
        self.assertTrue(self.table.seats[1].equity == 10)
        self.assertTrue(self.table.pots[-1].side_pots[0] == 10)

    def test_min_raise(self):
        """ Can we ensure that players cant raise less than the min? """
        with self.assertRaises(Exception) as context:
            self.table.seats[1].bet(1)
        self.assertIn("Minimum raise is 2", str(context.exception))

    def test_max_bet_is_all_in(self):
        """ Can we ensure that players cant bet/raise more than their stack? """
        with self.assertRaises(Exception) as context:
            self.table.seats[1].bet(200)
        self.assertIn("You can only bet what you have on the table!!", str(context.exception))

    def test_bet_increment_adjusted(self):
        """ Can we set/adjust the bet increment appropriately? """
        self.table.seats[1].bet(50)
        self.assertEqual(self.table.bet_increment, 50)

    def test_fold(self):
        """ Can we fold a player out?"""
        self.table.seats[1].action = True
        self.table.seats[1].fold()
        self.assertNotIn(self.table.seats[1], self.table.pots[0].players)
        self.assertNotIn(self.table.seats[1], self.table.pots[1].players)


if __name__ == '__main__':
    unittest.main()
