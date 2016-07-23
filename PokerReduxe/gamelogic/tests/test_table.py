__author__ = 'mark'
import unittest
from player import Player
from table import Table
from dealer import Dealer
from seat import Seat
from pot import Pot


class TestTable(unittest.TestCase):
    """Do we have a working table object?"""

    def setUp(self):
        self.p0 = Player('p0', 100)
        self.p1 = Player('p1', 100)
        self.p2 = Player('p2', 100)
        self.p3 = Player('p3', 100)
        self.p4 = Player('p4', 100)
        self.p5 = Player('p5', 100)

        self.s0 = Seat('s0')
        self.s1 = Seat('s1')
        self.s2 = Seat('s2')
        self.s3 = Seat('s3')
        self.s4 = Seat('s4')
        self.s5 = Seat('s5')

        players = [self.p0, self.p1, self.p2, self.p3, self.p4, self.p5]
        seats = [self.s0, self.s1, self.s2, self.s3, self.s4, self.s5]

        self.table = Table(seats, 5, 10, 0)
        self.dealer = Dealer(self.table)
        self.table.dealer = self.dealer

        player = 0
        for seat in seats:
            seat.player = players[player]
            seat.player.seat = seat
            seat.active = True
            seat.player.table = self.table
            player += 1

    def test_set_button(self):
        """can we randomly set the button for initial play on active seats only??"""
        self.table.seats[2].active = False
        self.table.set_button()
        a = self.table.button
        self.assertTrue(self.table.seats[self.table.button].active)
        self.table.set_button()
        b = self.table.button
        self.assertTrue(self.table.seats[self.table.small_blind].active)
        self.table.set_button()
        c = self.table.button
        self.assertTrue(self.table.seats[self.table.big_blind].active)
        self.table.set_button()
        d = self.table.button
        self.assertTrue(self.table.seats[self.table.under_the_gun].active)
        self.table.set_button()
        e = self.table.button
        self.assertTrue(self.table.seats[self.table.button].active)
        self.table.set_button()
        f = self.table.button
        self.assertTrue(self.table.seats[self.table.button].active)
        self.assertFalse(a == b and b == c and
                         c == d and d == e and e == f)

        """can we set the button/blinds correctly head to head?"""

        self.table.seats[3].active = False
        self.table.seats[2].active = False
        self.table.seats[4].active = False
        self.table.seats[5].active = False
        self.table.set_button()
        self.assertEqual(self.table.button, self.table.small_blind)
        self.assertEqual(self.table.button, self.table.under_the_gun)
        self.assertFalse(self.table.button == self.table.big_blind)

    def test_button_move(self):
        """Can we move the button and the blinds appropriately?"""
        self.table.button = 5
        self.table.small_blind = 0
        self.table.big_blind = 1
        self.table._button_move()
        self.assertEqual(self.table.button, 0)
        self.assertEqual(self.table.small_blind, 1)
        self.assertEqual(self.table.big_blind, 2)
        self.assertEqual(self.table.under_the_gun, 3)

    def test_skip_inactive(self):
        self.table.button = 5
        self.table.small_blind = 0
        self.table.big_blind = 1
        self.s2.active = False
        self.table._button_move()
        self.assertFalse(self.table.big_blind == 2)

    def test_dead_sb(self):
        """if the big blind goes inactive do we get a dead small blind?"""
        self.s1.active = False
        self.p1.missed_big_blind = False
        self.table.button = 5
        self.table.small_blind = 0
        self.table.big_blind = 1
        self.table._button_move()
        self.assertTrue(self.table.small_blind == 1)

    def test_button_move_head_to_head(self):
        """Can we move the blinds and button appropriately head to head?"""
        self.s2.active = False
        self.p2.missed_big_blind = True
        self.s3.active = False
        self.p3.missed_big_blind = True
        self.s4.active = False
        self.p4.missed_big_blind = True
        self.s5.active = False
        self.p5.missed_big_blind = True
        self.table.button = 2
        self.table.small_blind = 3
        self.table.big_blind = 0
        self.table._button_move()
        self.assertEqual(self.table.button, 0)
        self.assertEqual(self.table.small_blind, 0)
        self.assertEqual(self.table.big_blind, 1)
        self.assertEqual(self.table.under_the_gun, 0)

    def test_set_missed_bb(self):
        """Do we set the players missed bb appropriately?"""
        self.table.button = 5
        self.table.small_blind = 0
        self.table.big_blind = 1
        self.s2.active = False
        self.table._button_move()

        self.assertTrue(self.p2.missed_big_blind)
        self.assertFalse(self.p2.missed_small_blind)

    def test_set_missed_sb(self):
        """Do we set the players missed sb appropriatly?"""
        self.table.button = 0
        self.table.small_blind = 1
        self.table.big_blind = 3
        self.s2.active = False
        self.p2.missed_big_blind = True
        self.table._button_move()
        self.assertTrue(self.p2.missed_small_blind)

    def test_buying_the_button(self):
        """first active seat between buttons and sb should buy
        the button, all others should be frozen"""
        self.table.button = 0
        self.p1.missed_big_blind = True
        self.p2.missed_big_blind = True
        self.table.small_blind = 3
        self.table.big_blind = 4

        self.table._reset_blinds()
        self.assertTrue(self.table.bought_button == 1)
        self.assertTrue(self.p2.frozen)

    def test_button_buy_pays(self):
        """The bb and sb don't pay after a button buy"""
        self.table.button = 0
        self.table.bought_button = 1
        self.table.small_blind = 2
        self.table.big_blind = 3
        self.table._create_pot()

        self.assertTrue(self.p2.stack == 100)
        self.assertTrue(self.p3.stack == 100)
        self.assertTrue(self.p1.stack == 85)

    def test_create_pot(self):
        """ can we spawn a pot object properly? """
        self.table.small_blind = 0
        self.table.big_blind = 1
        self.table.utg = 2
        self.p0.missed_big_blind = True
        self.p4.missed_big_blind = True
        self.p4.missed_small_blind = True
        pot = self.table._create_pot()

        self.assertEqual(pot.pot, 40)
        self.assertEqual(len(self.table.pots), 1)
        self.assertEqual(pot.increment, self.table.big_blind_amount)

    def test_reset_players(self):
        """ Can we reset for a new hand??"""
        self.table.seats[0].player.equity = 50
        self.table.seats[0].player.hole = [1, 2, 3]
        self.table._reset_players()
        self.assertTrue(self.table.seats[0].player.equity == 0)
        self.assertEqual(len(self.table.seats[0].player.hole), 0)

    def test_reset_frozen_seat(self):
        """ Can we reset dead button player to active"""
        self.table.seats[4].active = False
        self.table.seats[4].player.frozen = True
        self.table._reset_players()

        self.assertTrue(self.table.seats[4].active)
        self.assertFalse(self.table.seats[4].player.frozen)

    def test_remove_0_stack(self):
        """Does the table remove broke players at the start of a hand??"""
        self.setUp()
        self.table.seats[2].player.stack = 0
        self.table._remove_0_stack()
        self.assertFalse(self.table.seats[2].active)

    def test_init_hand(self):
        """Does it all come together?"""
        self.p0.stack = 0
        self.table.init_hand()
        self.assertTrue(self.table.pots[0].pot == 15)
        self.assertEqual(len(self.p1.hole), 2)

if __name__ == '__main__':
    unittest.main()
