import unittest

import app
from player import Player
from pot import Pot
from table import Table


class TestApp(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("player1", 100)
        self.player2 = Player("player2", 100)
        self.player3 = Player("player3", 100)
        self.player4 = Player("player4", 100)
        self.player5 = Player("player5", 100)
        self.player6 = Player("player6", 100)

        self.table = Table(6, 1, 2, [50, 100])

        self.table.join(1, self.player1, 100)
        self.table.join(2, self.player2, 100)
        self.table.join(3, self.player3, 100)
        self.table.join(4, self.player4, 100)
        self.table.join(5, self.player5, 100)
        self.table.join(6, self.player6, 100)

        # Set player order; happy path
        for k, v in self.table.seats.items():
            self.table.player_order.append(v)

        pot = Pot(self.table.player_order, 0)

        self.table.pots.append(pot)

    def test_get_active_players(self):
        """ Can we grab a list of active players? """
        six_players = app.get_active_players(self.table)
        self.player1.active = False
        five_players = app.get_active_players(self.table)
        self.assertEqual(6, len(six_players))
        self.assertEqual(5, len(five_players))

    def test_remove_broke_player(self):
        """ Can we remove players with zero chips left in stack """
        self.player1.stack = 0
        five_players = app.get_active_players(self.table)
        self.assertEqual(5, len(five_players))

    def test_set_button(self):
        """ Can we randomly set the button? """
        call1 = app.set_button(self.table)[:]
        call2 = app.set_button(self.table)[:]
        call3 = app.set_button(self.table)[:]
        call4 = app.set_button(self.table)[:]
        call5 = app.set_button(self.table)[:]

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
        self.player2.acted = True
        app.move_button(self.table)
        self.assertTrue(self.player2.missed_sb)

    def test_remove_missed_blinds_from_button(self):
        """ Can we remove people who owe blinds in the button position? """
        self.player6.missed_bb = True
        self.player5.missed_sb = True
        app.missed_blind_corner_cases(self.table)
        self.assertEqual(4, len(self.table.player_order))

    def test_bought_button(self):
        """ Can we appropriately allow someone to buy the button? """
        self.player1.missed_bb = True
        app.missed_blind_corner_cases(self.table)
        self.assertEqual(3, self.player1.equity)
        self.assertEqual(0, self.player2.equity)

    def test_only_one_bought_button(self):
        """ Can we ensure only one bought button? """
        self.player1.missed_bb = True
        self.player2.missed_bb = True
        app.missed_blind_corner_cases(self.table)
        self.assertEqual(5, len(self.table.player_order))

    def test_collect_all_blinds(self):
        """ Can we collect all of the blinds? """
        app.collect_blinds(self.table)
        self.assertEqual(99, self.player1.stack)
        self.assertEqual(1, self.player1.equity)
        self.assertEqual(98, self.player2.stack)
        self.assertEqual(2, self.player2.equity)

    def test_collect_blinds_head_to_head(self):
        """ Can we set/collect the blinds for head to head appropriately? """
        self.table.player_order = [self.player1, self.player2]
        app.collect_blinds(self.table)
        self.assertEqual(99, self.player2.stack)
        self.assertEqual(1, self.player2.equity)
        self.assertEqual(98, self.player1.stack)
        self.assertEqual(2, self.player1.equity)

    def test_dont_collect_blinds_if_button_has_been_bought(self):
        """ Can we ensure that we dont collect bb if button is bought """
        self.player1.equity = 3
        app.collect_blinds(self.table)
        self.assertEqual(3, self.player1.equity)
        self.assertEqual(0, self.player2.equity)

    def test_collect_missed_blinds(self):
        """ Can we ensure that missed blinds are collected? """
        self.player3.missed_sb = True
        self.player3.missed_bb = True
        self.player4.missed_bb = True
        self.player5.missed_sb = True
        app.collect_missed_blinds(self.table)
        self.assertEqual(3, self.player3.equity)
        self.assertEqual(98, self.player4.stack)
        self.assertEqual(False, self.player5.missed_sb)

    def test_create_initial_pot(self):
        """ Can we ensure a proper initial pot is created? """
        self.table.pots = []
        self.player3.equity = 3
        self.player4.equity = 2
        self.player5.stack = 10
        self.table.ante = 10
        app.create_initial_pot(self.table)
        self.assertEqual(12, self.player3.equity)
        self.assertEqual(61, self.table.pots[0].amount)
        self.assertEqual(10, self.table.pots[0].side_pots[0])

    def test_deck_is(self):
        """ Can we ensure that we have a full deck? """
        app.create_deck(self.table)
        self.assertEqual(52, len(self.table.deck))
        unique_deck = self.table.deck[:]
        unique_deck = set(unique_deck)
        unique_deck = list(unique_deck)
        self.assertEqual(52, len(unique_deck))
        spades = [x for x in self.table.deck if x.suit == "s"]
        self.assertEqual(13, len(spades))
        unique_deck = list(set(spades))
        self.assertEqual(13, len(unique_deck))

    def test_deal_hole_cards(self):
        """ Can we ensure hole cards are dealt appropriately """
        app.deal_hole(self.table)
        x = 0
        for player in self.table.player_order:
            if len(player.hole_cards) == 2:
                x += 1
        self.assertEqual(x, 6)
        self.assertEqual(40, len(self.table.deck))

    def test_action_time_first_to_act(self):
        """ If player has yet to play, can we set its action to True? """
        app.action_time(self.table)
        self.assertTrue(self.player1.action)

    def test_action_time_second_pass(self):
        """ If player has already acted, and been raised, can we set its action to True? """
        self.table.current_bet = 20
        self.player1.equity = 10
        self.player1.acted = True
        app.action_time(self.table)
        self.assertTrue(self.player1.action)

    def test_action_time_skip_all_in_player(self):
        """ Can we skip an all in player? """
        self.player1.stack = 0
        app.action_time(self.table)
        self.assertFalse(self.player1.action)
        self.assertTrue(self.player2.action)

    def test_evaluate_pot_creates_side_pots(self):
        """ Can we create and append side pots appropriately? """
        self.player1.stack = 0
        self.player1.equity = 10
        self.player2.stack = 0
        self.player2.equity = 20
        self.player3.stack = 0
        self.player3.equity = 30
        self.player4.stack = 0
        self.player4.equity = 40
        self.player5.stack = 100
        self.player5.equity = 50
        self.player6.stack = 100
        self.player6.equity = 50

        app.create_deck(self.table)

        self.table.pots[-1].side_pots = [10, 40, 20, 30]
        self.table.pots[-1].amount = 1000
        app.evaluate_pot(self.table)
        self.assertEqual(2, len(self.table.pots[-1].players))
        self.assertEqual(1060, self.table.pots[-2].amount)


if __name__ == '__main__':
    unittest.main()
