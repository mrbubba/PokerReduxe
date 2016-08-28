import unittest

import analyze
import app
from card import Card
from player import Player
from pot import Pot
from table import Table


class TestAnalyze(unittest.TestCase):
    def setUp(self):

        self.player1 = Player("player1", 100)
        self.player2 = Player("player2", 100)
        self.player3 = Player("player3", 100)
        self.player4 = Player("player4", 100)
        self.player5 = Player("player5", 100)
        self.player6 = Player("player6", 100)
        self.player7 = Player("player7", 100)
        self.player8 = Player("player8", 100)
        self.player9 = Player("player9", 100)

        self.table = Table(9, 1, 2, [50, 100])

        self.table.join(1, self.player1, 100)
        self.table.join(2, self.player2, 100)
        self.table.join(3, self.player3, 100)
        self.table.join(4, self.player4, 100)
        self.table.join(5, self.player5, 100)
        self.table.join(6, self.player6, 100)
        self.table.join(7, self.player7, 100)
        self.table.join(8, self.player8, 100)
        self.table.join(9, self.player9, 100)

        cards = [13, 'h', 14, 'h', 5, 'h', 5, 's', 5, 'h', 10, 'c', 3, 'h', 4,
                 'h', 13, 's', 14, 's', 14, 's', 5, 's', 12, 's',
                 11, 's', 14, 's', 2, 'd', 4, 'h', 2, 'h']

        # Set player order; happy path
        for k, v in self.table.seats.items():
            self.table.player_order.append(v)

        x = 0
        for player in self.table.player_order:
            value = cards[x]
            x += 1
            suit = cards[x]
            x += 1
            card0 = Card("name", value, suit)
            value = cards[x]
            x += 1
            suit = cards[x]
            x += 1
            card1 = Card("name", value, suit)
            player.hole_cards.append(card0)
            player.hole_cards.append(card1)

        table_cards = [12, 'h', 11, 'h', 10, 'h', 5, 'c', 5, 'd']
        x = 0
        while len(self.table.community_cards) != 5:
            value = table_cards[x]
            x += 1
            suit = table_cards[x]
            x += 1
            card = Card("name", value, suit)
            self.table.community_cards.append(card)
        pot = Pot(self.table.player_order, 100)

        self.table.pots.append(pot)

    def test_setup(self):
        """ Do we join the hole cards with the community cards? """
        analyze.setup(self.table)
        self.assertEqual(7, len(self.player1.hole_cards))
        self.assertEqual(7, len(self.player2.hole_cards))

    def test_order(self):
        """ Can we order the hands in a proper order, left to right """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        for player in pot.players:
            for i in range(6):
                v1 = player.hole_cards[i].value
                v2 = player.hole_cards[i + 1].value
                self.assertTrue(v2 <= v1)

    def test_flush(self):
        """ Can we find a flush in the players' hands """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.flush(pot)
        expected3 = [5, 12, 11, 10, 4, 3]
        expected8 = [5, 12, 11, 10, 4, 2]
        self.assertEqual(expected3, pot.players[3].hand)
        self.assertEqual(expected8, pot.players[8].hand)

    def test_flush_returns_card_values(self):
        """ For all none flush hands do we return card
        values instead of card objects """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.flush(pot)
        analyze.convert_to_card_value(pot)
        for player in pot.players:
            if not player.hand:
                for card in player.hole_cards:
                    self.assertIsInstance(card, int)

    def test_straight(self):
        """ Can we identify the highest straight in a hand """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.convert_to_card_value(pot)
        expected = [4, 14]
        self.assertEqual(expected, pot.players[4].hand)

    def test_wheel(self):
        """ Can we identify a wheel? """
        pot = analyze.setup(self.table)
        pot.players[4].hole_cards[0].value = 14
        pot.players[4].hole_cards[1].value = 4
        self.table.community_cards[0].value = 3
        self.table.community_cards[1].value = 2
        analyze.order(pot)
        analyze.convert_to_card_value(pot)
        expected = [4, 5]
        self.assertEqual(expected, pot.players[4].hand)

    def test_straight_flush(self):
        """ Can we identify a straight flush? """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.flush(pot)
        expected = [8, 14]
        self.assertEqual(expected, pot.players[0].hand)

    def test_4_of_a_kind(self):
        """ Can we identify a hand with four of a kind in proper format? """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.convert_to_card_value(pot)
        analyze.matching(pot)
        expected = [7, 5, 12]
        self.assertEqual(expected, pot.players[1].hand)

    def test_3_of_a_kind(self):
        """ Can we identify a hand with 3 of a kind in proper format? """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.convert_to_card_value(pot)
        analyze.matching(pot)
        expected = [3, 5, 14, 12]
        self.assertEqual(expected, pot.players[5].hand)

    def test_full_house(self):
        """ Can we identify a hand with a full house? """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.convert_to_card_value(pot)
        analyze.matching(pot)
        expected = [6, 5, 10]
        self.assertEqual(expected, pot.players[2].hand)

    def test_compare(self):
        """ Can we determine a single winner? """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.flush(pot)
        analyze.convert_to_card_value(pot)
        analyze.matching(pot)
        analyze.compare(pot)
        expected = self.player1
        self.assertEqual(expected, pot.players[-1])
        self.assertTrue(len(pot.players) == 1)

    def test_compare_multiple(self):
        """ if there are multiple winners do we return all of them? """
        pot = analyze.setup(self.table)
        pot.players[1].hole_cards[0].value = 14
        pot.players[1].hole_cards[0].suit = 'h'
        pot.players[1].hole_cards[1].value = 13
        pot.players[1].hole_cards[1].suit = 'h'
        analyze.order(pot)
        analyze.flush(pot)
        analyze.convert_to_card_value(pot)
        analyze.matching(pot)
        analyze.compare(pot)
        expected = [self.player1, self.player2]
        self.assertEqual(expected, pot.players)

    def test_award(self):
        """ can we award a single winner the entire pot? """
        pot = analyze.setup(self.table)
        analyze.order(pot)
        analyze.flush(pot)
        analyze.convert_to_card_value(pot)
        analyze.matching(pot)
        analyze.compare(pot)
        analyze.award(pot, self.table.sb_amount)
        self.assertTrue(self.player1.stack == 200)
        self.assertTrue(len(pot.players) == 1)

    def test_award_multiple(self):
        """ Can we pay out evenly to multiple winners """
        pot = analyze.setup(self.table)
        pot.players[1].hole_cards[0].value = 14
        pot.players[1].hole_cards[0].suit = 'h'
        pot.players[1].hole_cards[1].value = 13
        pot.players[1].hole_cards[1].suit = 'h'
        analyze.order(pot)
        analyze.flush(pot)
        analyze.convert_to_card_value(pot)
        analyze.matching(pot)
        analyze.compare(pot)
        analyze.award(pot, self.table.sb_amount)
        expected = [self.player1, self.player2]
        self.assertEqual(expected, pot.players)

    def test_award_indivisible(self):
        """Can we properly pay pots that don't divide
        evenly?"""
        pot = analyze.setup(self.table)
        pot.amount = 101
        pot.players[1].hole_cards[0].value = 14
        pot.players[1].hole_cards[0].suit = 'h'
        pot.players[1].hole_cards[1].value = 13
        pot.players[1].hole_cards[1].suit = 'h'
        analyze.order(pot)
        analyze.flush(pot)
        analyze.convert_to_card_value(pot)
        analyze.matching(pot)
        analyze.compare(pot)
        analyze.award(pot, self.table.sb_amount)
        expected1 = 151
        expected2 = 150
        self.assertEqual(expected1, pot.players[0].stack)
        self.assertEqual(expected2, pot.players[1].stack)

    def test_analyze(self):
        """ Will analyzer run appropriately? """
        pot = self.table.pots[-1]
        pot.amount = 101
        pot.players[1].hole_cards[0].value = 14
        pot.players[1].hole_cards[0].suit = 'h'
        pot.players[1].hole_cards[1].value = 13
        pot.players[1].hole_cards[1].suit = 'h'
        analyze.analyze(self.table)
        expected1 = 151
        expected2 = 150
        self.assertEqual(expected1, pot.players[0].stack)
        self.assertEqual(expected2, pot.players[1].stack)


if __name__ == '__main__':
    unittest.main()
