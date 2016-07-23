import unittest


from table import Table
from player import Player
from madehand import MadeHand, HandUnit
from seat import Seat
from deck import Card


class TestMadeHand(unittest.TestCase):
    def setUp(self):
        self.player = Player('a_player', 100)
        self.seats = [Seat("a_seat")]
        self.table = Table(self.seats, 5, 10, 0)
        self.c1 = Card("c1", 2, "h")
        self.c2 = Card("c2", 2, "d")
        self.c3 = Card("c3", 3, "h")
        self.c4 = Card("c4", 7, "h")
        self.c5 = Card("c5", 7, "h")
        self.c6 = Card("c6", 7, "h")
        self.c7 = Card("c7", 7, "h")
        self.player.hole = [self.c1, self.c2]
        self.table.community_cards = [self.c3, self.c4, self.c5, self.c6, self.c7]
        self.madehand = MadeHand(self.table, self.player)

    def test_matching_values(self):
        """Can we return a dictionary with a count of each value in the hand"""
        seen = self.madehand._matching_values()
        self.assertTrue(seen[3] == 1)
        self.assertTrue(seen[2] == 2)
        self.assertTrue(seen[7] == 4)

    def test_isQuads(self):
        """Can we set the quads list properly ( setup here has a quad in it)"""
        seen = self.madehand._matching_values()
        self.madehand._is_quads(seen)
        self.assertTrue(self.player.handunit.quads['face_value'] == 7)

    def test_isQuads_shared(self):
        """Can we tell if the quads are community or in the hand, if community append the Kicker to the quads list"""
        seen = self.madehand._matching_values()
        self.madehand._is_quads(seen)
        self.assertTrue(self.player.handunit.quads['hole'] > 0)

    def test_isQuads_kicker_shared(self):
        """Can we tell if the Kicker on board quads is shared"""
        seen = self.madehand._matching_values()
        self.madehand._is_quads(seen)
        self.assertTrue(self.player.handunit.quads['hole_kicker'] == False)

    def test_isQuads_kicker_not_shared(self):
        """ Can we tell if the kicker on board quads is not shared
        """
        self.c1.value = 12
        seen = self.madehand._matching_values()
        self.madehand._is_quads(seen)
        self.assertTrue(self.player.handunit.quads['hole_kicker'] == True)

    def test_isTrips(self):
        """Can we set the quads list properly ( setup here has a quad in it)"""
        self.c7.value = 8
        seen = self.madehand._matching_values()
        self.madehand._is_trips(seen)
        self.assertTrue(self.player.handunit.trips['face_value'] == 7)

    def test_is_trips2(self):
        pass

    def test_number_cards_in_hole(self):
        """Can we determine how many of the trip cards are in the hole?"""
        pass

if __name__ == '__main__':
    unittest.main()
