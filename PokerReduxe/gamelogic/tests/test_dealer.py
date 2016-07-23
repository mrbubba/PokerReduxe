import unittest


from deck import Deck
from player import Player
from table import Table
from dealer import Dealer
from seat import Seat


class TestDeck(unittest.TestCase):
    """Do We have a working deck??"""

    def setUp(self):
        self.deck = Deck()
        self.deck.create()

    def test_create(self):
        """Can we create a deck?"""
        self.assertTrue(len(self.deck.deck) == 52)
        self.assertFalse(self.deck.deck[0].name == self.deck.deck[1].name)

    def test_deal(self):
        dealt_card = self.deck.deck[0]
        next_card = self.deck.deck[1]
        result = self.deck.deal()
        self.assertEqual(result, dealt_card)
        self.assertEqual(self.deck.deck[0], next_card)


class TestDealer(unittest.TestCase):
    """Do we have a functioning Dealer?"""

    def setUp(self):
        self.p1 = Player('p1', 100)
        self.p2 = Player('p2', 100)
        self.p3 = Player('p3', 0)
        self.p4 = Player('p4', 100)

        self.s1 = Seat('s1')
        self.s2 = Seat('s2')
        self.s3 = Seat('s3')
        self.s4 = Seat('s4')

        players = [self.p1, self.p2, self.p3, self.p4]
        seats = [self.s1, self.s2, self.s3, self.s4]

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

    def test_deal_hole(self):
        """can the dealer deal two cards to each player??"""
        self.table.seats[2].active = False
        self.table.init_hand()
        # only want the active players
        players = []
        for seat in self.table.seats:
            if seat.active:
                players.append(seat.player)
        # active players should have cards
        for player in players:
            self.assertEqual(len(player.hole), 2)
        # inactive players shouldn't have cards
        self.assertEqual(len(self.table.seats[2].player.hole), 0)

if __name__ == '__main__':
    unittest.main()
