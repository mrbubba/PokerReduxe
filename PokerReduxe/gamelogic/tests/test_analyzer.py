__author__ = 'mark'
import unittest
from player import Player
from table import Table
from dealer import Dealer
from seat import Seat
from analyzer import Analyzer


class TestAnalyzer(unittest.TestCase):

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

        self.table.init_hand()
        self.dealer.deal()
        self.dealer.deal()
        self.dealer.deal()
        self.analyzer = Analyzer(self.table)

    def test_award(self):
        """can we award a single winner the entire pot?"""
        players = [self.p2]
        self.table.pots[0].pot = 100
        self.p2.stack = 90
        self.analyzer._award(players)

        self.assertEqual(self.p2.stack, 190)

    def test_award_multiple(self):
        """Can we pay out evenly to multiple winners?"""
        players = [self.p2, self.p3]
        self.table.pots[0].pot = 100
        self.p2.stack = 50
        self.p3.stack = 50
        self.analyzer._award(players)

        self.assertEqual(self.p2.stack, 100)
        self.assertEqual(self.p3.stack, 100)

    def test_award_indivisible(self):
        """Can we properly pay pots that don't divide
        evenly?"""
        players = [self.p2, self.p3]
        self.table.first = 1
        self.table.pots[0].pot = 105
        self.p2.stack = 50
        self.p3.stack = 50
        self.analyzer._award(players)

        self.assertEqual(self.p2.stack, 105)
        self.assertEqual(self.p3.stack, 100)

    def test_compare(self):
        """can we determine the winning hand"""
        players = self.analyzer._setup()

        self.p0.hand = [0, 14, 12, 11, 10, 8]
        self.p1.hand = [1, 14, 12, 11, 8]
        self.p2.hand = [7, 8, 14]
        self.p3.hand = [7, 10, 2]
        self.p4.hand = [0]
        self.p5.hand = [0]

        result = self.analyzer._compare(players)
        expected = [self.p3]
        self.assertEqual(expected, result)

    def test_compare_multiple(self):
        """if there are multiple winners do we
        return all of them?"""
        players = self.analyzer._setup()

        self.p0.hand = [0, 14, 12, 11, 10, 8]
        self.p1.hand = [1, 14, 12, 11, 8]
        self.p2.hand = [7, 10, 2]
        self.p3.hand = [7, 10, 2]
        self.p4.hand = [0]
        self.p5.hand = [0]

        result = self.analyzer._compare(players)
        expected = [self.p2, self.p3]
        self.assertEqual(expected, result)

    def test_hi_card(self):
        """can we identify a hi card hand?"""
        players = self.analyzer._setup()

        self.p4.hole[0].value = 12
        self.p4.hole[1].value = 11
        self.p4.hole[2].value = 9
        self.p4.hole[3].value = 14
        self.p4.hole[4].value = 13
        self.p4.hole[5].value = 3
        self.p4.hole[6].value = 2

        players = self.analyzer._order(players)

        self.analyzer._matching(players)

        expected = [0, 14, 13, 12, 11, 9]
        self.assertEqual(self.p4.hand, expected)

    def test_matching_hands(self):
        """can we find matching number hands
         eg.  pairs through quads??"""
        players = self.analyzer._setup()

        # quads
        self.p0.hole[0].value = 14
        self.p0.hole[1].value = 14

        # boat
        self.p1.hole[0].value = 14
        self.p1.hole[1].value = 13

        # trips
        self.p2.hole[0].value = 14
        self.p2.hole[1].value = 12

        # two pair
        self.p3.hole[0].value = 12
        self.p3.hole[1].value = 12

        # pair
        self.p4.hole[0].value = 12
        self.p4.hole[1].value = 11

        self.p4.hole[2].value = 14
        self.p4.hole[3].value = 14
        self.p4.hole[4].value = 13
        self.p4.hole[5].value = 3
        self.p4.hole[6].value = 2

        players = self.analyzer._order(players)

        self.analyzer._matching(players)

        # Do we have 4 A's with a K kicker?
        self.assertEqual(self.p0.hand, [7, 14, 13])
        # Do we have a boat A's full of K's?
        self.assertEqual(self.p1.hand, [6, 14, 13])
        # Do we have trip A's with K & Q kickers?
        self.assertEqual(self.p2.hand, [3, 14, 13, 12])
        # Do we have 2 pair A's & Q's with a K kicker?
        self.assertEqual(self.p3.hand, [2, 14, 12, 13])
        # Do we have a pair of A's with K, Q, J kickers?
        self.assertEqual(self.p4.hand, [1, 14, 13, 12, 11])

    def test_straight(self ):
        """can we find the highest straight in a hand"""
        players = self.analyzer._setup()
        #p0 has a 6 high straight
        self.p0.hole[0].value = 8
        self.p0.hole[1].value = 6
        self.p0.hole[2].value = 5
        self.p0.hole[3].value = 4
        self.p0.hole[4].value = 3
        self.p0.hole[5].value = 13
        self.p0.hole[6].value = 2
        #poor p1 hit the wheel
        self.p1.hole[0].value = 14
        self.p1.hole[1].value = 11

        self.analyzer._order(players)

        self.analyzer._straight(self.p0)
        self.analyzer._straight(self.p1)
        expected_0 = [4, 6]
        expected_1 = [4, 5]
        self.assertEqual(self.p0.hand, expected_0)
        self.assertEqual(self.p1.hand, expected_1)

    def test_flush(self):
        """Can we find a flush in the players' hands"""
        players = self.analyzer._setup()
        # a flush
        self.p0.hole[0].suit = "d"
        self.p0.hole[0].value = 2
        self.p0.hole[1].suit = "d"
        self.p0.hole[1].value = 2
        self.p0.hole[2].suit = "d"
        self.p0.hole[3].suit = "d"
        self.p0.hole[4].suit = "d"
        self.p0.hole[5].suit = "d"
        self.p0.hole[5].value = 5
        self.p0.hole[6].suit = "d"
        self.p0.hole[6].value = 4

        self.p1.hole[0].suit = "d"
        self.p1.hole[1].suit = "d"
        self.p1.hole[0].value = 14
        self.p1.hole[1].value = 13
        self.p1.hole[2].value = 12
        self.p1.hole[3].value = 11
        self.p1.hole[4].value = 10
        players = self.analyzer._order(players)

        self.analyzer._flush(players)
        self.assertTrue(self.p0.hand)
        self.assertEqual(self.p0.hand[0], 5)
        self.assertEqual(len(self.p0.hand), 6)
        # p1 should be a straight flush
        expected = [8, 14]
        self.assertEqual(self.p1.hand, expected)

    def test_order(self):
        """Can we order the hands in a proper order, left to right"""
        players = self.analyzer._setup()

        players = self.analyzer._order(players)
        for player in players:
            for i in range(6):
                v1 = player.hole[i].value
                v2 = player.hole[i + 1].value
                self.assertTrue(v2 <= v1)

    def test_seven_cards(self):
        """Can we get a list of players in the hand with 7 cards in the hand"""
        players = self.analyzer._setup()
        for player in players:
            self.assertTrue(len(player.hole) == 7)

if __name__ == '__main__':
    unittest.main()
