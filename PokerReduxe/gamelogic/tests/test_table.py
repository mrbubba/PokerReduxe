import unittest

from PokerReduxe.gamelogic.table import Table



class TestTable(unittest.TestCase):
    """ Do we have a working table object? """

    def setUp(self):
        self.table = Table("Table", 6, 1, 2, [50, 100])

    def test_seats_dict(self):
        """ Is seats dict properly created on instantiation """
        self.assertEqual(len(self.table.seats), 6)

    def test_seats_dict_exception(self):
        """ Do we throw an error when too many seats """
        with self.assertRaises(ValueError):
            Table("Table", 12, 1, 2, [50, 10])

    def test_join_table(self):
        """Can a player join our table??"""
        self.assertFalse(self.table.seats[1])
        self.table.join(1, 'player1', 100)
        self.assertTrue(self.table.seats[1])

    def test_join_taken_seat(self):
        """Can a player take an already filled spot??  We hope not!!"""
        self.table.join(1, 'player1', 100)
        with self.assertRaises(ValueError):
            self.table.join(2, self.table.seats[1].name, 100)
        self.assertTrue(self.table.seats[1].name == self.table.seats[1].name)

    def test_player_can_only_have_one_seat_at_the_table(self):
        """A player should only occupy one seat per table."""
        self.table.join(1, self.table.seats[1], 100)
        with self.assertRaises(ValueError):
            self.table.join(2, self.table.seats[1].name, 100)
        self.assertFalse(self.table.seats[2])

    def test_set_player_buyin(self):
        """can set players stack with buy in"""
        self.table.join(1, 'player1', 100)
        self.assertEqual(self.table.seats[1].stack, 100)

    def test_set_buyin_range(self):
        """Can we restrict players to the table buyin range?"""
        with self.assertRaises(ValueError):
            self.table.join(1, self.table.seats[1], 110)
        self.assertFalse(self.table.seats[1])

    def test_quit(self):
        """ Can a player quit the game? """
        self.table.join(1, 'player1', 100)
        self.table.quit(self.table.seats[1])
        self.assertFalse(self.table.seats[1])

    def test_no_change_to_occupied_seat(self):
        """ Can we prevent a player from sitting in an occupied seat? """
        self.table.join(1, 'player1', 100)
        self.table.join(2, 'player2', 100)
        with self.assertRaises(Exception) as context:
            self.table.change_seat(self.table.seats[1], 2)
        self.assertIn("This seat is occupied!!", str(context.exception))

    def test_change_seat_range(self):
        """ Does the seat in question exist? """
        self.table.join(1, 'player1', 100)
        self.table.join(2, 'player2', 100)
        with self.assertRaises(Exception) as context:
            self.table.change_seat(self.table.seats[1], 13)
        self.assertIn("This seat doesn't exist!!", str(context.exception))

    def test_change_seat(self):
        """ Can a player change to an open seat? """
        self.table.join(1, 'player1', 100)
        self.table.join(2, 'player2', 100)
        self.table.player_order = [self.table.seats[1], self.table.seats[2]]
        self.table.change_seat(self.table.seats[1], 3)
        self.assertEqual('player1', self.table.seats[3].name)
        self.assertFalse(self.table.seats[1])

if __name__ == '__main__':
    unittest.main()
