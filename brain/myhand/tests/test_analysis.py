import unittest

from brain.myhand.hand_analysis import *
from gameserver.gamelogic.card import Card


class TestAnalyze(unittest.TestCase):
    def test_cards_are_properly_removed_from_deck(self):
        common_cards = []
        common_cards.append(Card("Ace_Diamonds", 14, "d"))
        common_cards.append(Card("Ace_Hearts", 14, "h"))
        common_cards.append(Card("Ace_Spades", 14, "s"))
        common_cards.append(Card("Ace_Clubs", 14, "c"))

        hand_order(common_cards)

        self.assertEqual(len(deck), 48)


if __name__ == '__main__':
    unittest.main()
