import unittest

import PokerReduxe.gamelogic.app as app
from PokerReduxe.gamelogic.pot import Pot
from PokerReduxe.gamelogic.table import Table


class TestApp(unittest.TestCase):
    def setUp(self):
        self.table = Table("Table", 6, 1, 2, [50, 100])

        self.table.join(1, 'player1', 100)
        self.table.join(2, 'player2', 100)
        self.table.join(3, 'player3', 100)
        self.table.join(4, 'player4', 100)
        self.table.join(5, 'player5', 100)
        self.table.join(6, 'player6', 100)

        # Set player order; happy path
        for k, v in self.table.seats.items():
            self.table.player_order.append(v)

        pot = Pot(self.table.player_order, 0)

        self.table.pots.append(pot)

    def test_get_active_players(self):
        """ Can we grab a list of active players? """
        six_players = app.get_active_players(self.table)
        self.table.seats[1].active = False
        five_players = app.get_active_players(self.table)
        self.assertEqual(6, len(six_players))
        self.assertEqual(5, len(five_players))

    def test_remove_broke_player(self):
        """ Can we remove players with zero chips left in stack """
        self.table.seats[1].stack = 0
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
        self.table.seats[4].active = False
        app.move_button(self.table)
        self.assertEqual(len(self.table.player_order), 5)

    def test_add_player_to_hand(self):
        """ Can we add a new player to hand appropriately """
        expected = self.table.player_order[:]
        x = expected.pop(0)
        expected.append(x)
        x = expected.pop(0)
        expected.append(x)
        self.table.seats[4].active = False
        app.move_button(self.table)
        self.table.seats[4].active = True
        app.move_button(self.table)
        self.assertEqual(len(self.table.player_order), 6)
        self.assertEqual(expected, self.table.player_order)
        self.assertTrue(self.table.seats[4] == self.table.player_order[1])

    def test_bb_mia(self):
        """ Can we prepend sb position to None if bb goes mia """
        self.table.player_order[1].active = False
        app.move_button(self.table)
        self.assertEqual(self.table.player_order[0], None)
        expected = self.table.player_order[:]
        expected.pop(0)
        expected.insert(0, None)
        app.move_button(self.table)
        self.assertEqual(expected, self.table.player_order)

    def test_set_missed_bb(self):
        """ Can we set missed bb to True """
        self.table.seats[3].active = False
        app.move_button(self.table)
        self.assertTrue(self.table.seats[3].missed_bb)

    def test_set_missed_sb(self):
        """ Can we set missed sb to True """
        self.table.seats[2].active = False
        app.move_button(self.table)
        self.assertTrue(self.table.seats[2].missed_sb)

    def test_remove_missed_blinds_from_button(self):
        """ Can we remove people who owe blinds in the button position? """
        self.table.seats[6].missed_bb = True
        self.table.seats[1].missed_sb = True
        app.move_button(self.table)
        self.assertEqual(4, len(self.table.player_order))

    def test_bought_button(self):
        """ Can we appropriately allow someone to buy the button? """
        self.table.seats[2].missed_bb = True
        app.move_button(self.table)
        self.assertEqual(2, self.table.seats[2].equity)
        self.assertEqual(0, self.table.seats[3].equity)

    def test_only_one_bought_button(self):
        """ Can we ensure only one bought button? """
        self.table.seats[2].missed_bb = True
        self.table.seats[3].missed_bb = True
        app.move_button(self.table)
        self.assertEqual(5, len(self.table.player_order))

    def test_collect_all_blinds(self):
        """ Can we collect all of the blinds? """
        app.collect_blinds(self.table)
        self.assertEqual(99, self.table.seats[1].stack)
        self.assertEqual(1, self.table.seats[1].equity)
        self.assertEqual(98, self.table.seats[2].stack)
        self.assertEqual(2, self.table.seats[2].equity)

    def test_collect_blinds_head_to_head(self):
        """ Can we set/collect the blinds for head to head appropriately? """
        self.table.player_order = [self.table.seats[1], self.table.seats[2]]
        app.collect_blinds(self.table)
        self.assertEqual(99, self.table.seats[2].stack)
        self.assertEqual(1, self.table.seats[2].equity)
        self.assertEqual(98, self.table.seats[1].stack)
        self.assertEqual(2, self.table.seats[1].equity)

    def test_dont_collect_blinds_if_button_has_been_bought(self):
        """ Can we ensure that we dont collect bb if button is bought """
        self.table.seats[1].equity = 3
        self.table.bought_button = True
        app.collect_blinds(self.table)
        self.assertEqual(3, self.table.seats[1].equity)
        self.assertEqual(0, self.table.seats[2].equity)

    def test_collect_missed_blinds(self):
        """ Can we ensure that missed blinds are collected? """
        self.table.seats[3].missed_sb = True
        self.table.seats[3].missed_bb = True
        self.table.seats[4].missed_bb = True
        self.table.seats[5].missed_sb = True
        app.collect_missed_blinds(self.table)
        self.assertEqual(3, self.table.seats[3].equity)
        self.assertEqual(98, self.table.seats[4].stack)
        self.assertEqual(False, self.table.seats[5].missed_sb)

    def test_create_initial_pot(self):
        """ Can we ensure a proper initial pot is created? """
        self.table.pots = []
        self.table.seats[3].equity = 3
        self.table.seats[4].equity = 2
        self.table.seats[5].stack = 10
        self.table.ante = 10
        app.create_initial_pot(self.table)
        self.assertEqual(2, self.table.seats[3].equity)
        self.assertEqual(61, self.table.pots[0].amount)

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
        app.action_time(self.table.seats[6], self.table)
        self.assertTrue(self.table.seats[1].action)

    def test_action_time_second_pass(self):
        """ If player has already acted, and been raised, can we set its action to True? """
        self.table.current_bet = 20
        self.table.seats[1].equity = 10
        self.table.seats[1].acted = True
        app.action_time(self.table.seats[6], self.table)
        self.assertTrue(self.table.seats[1].action)

    def test_action_time_skip_all_in_player(self):
        """ Can we skip an all in player? """
        self.table.seats[1].stack = 0
        app.action_time(self.table.seats[6], self.table)
        self.assertFalse(self.table.seats[1].action)
        self.assertTrue(self.table.seats[2].action)

    def test_action_handle_pre_folder(self):
        """  Does action time fold out and skip a player that has folded out of turn?"""
        self.table.seats[2].folded = True
        app.action_time(self.table.seats[1], self.table)
        self.assertTrue(self.table.seats[2] not in self.table.pots[-1].players)
        self.assertTrue(self.table.seats[3].action)

    def test_evaluate_pot_creates_side_pots(self):
        """ Can we create and append side pots appropriately? """
        self.table.seats[1].stack = 0
        self.table.seats[1].equity = 10
        self.table.seats[2].stack = 0
        self.table.seats[2].equity = 20
        self.table.seats[3].stack = 0
        self.table.seats[3].equity = 30
        self.table.seats[4].stack = 0
        self.table.seats[4].equity = 40
        self.table.seats[5].stack = 100
        self.table.seats[5].equity = 50
        self.table.seats[6].stack = 100
        self.table.seats[6].equity = 50

        app.create_deck(self.table)

        self.table.pots[-1].side_pots = [10, 40, 20, 30]
        self.table.pots[-1].amount = 1000
        app.evaluate_pot(self.table)
        self.assertEqual(2, len(self.table.pots[-1].players))
        self.assertEqual(1060, self.table.pots[-2].amount)

    def test_evaluate_pot_ends_hand_when_1_player(self):
        """Do we end the hand and award the only hand the cash??"""
        self.table.pots[-1].players = [self.table.seats[1]]
        self.table.seats[1].equity = 50
        app.evaluate_pot(self.table)
        self.assertEqual(150, self.table.seats[1].stack)


if __name__ == '__main__':
    unittest.main()
