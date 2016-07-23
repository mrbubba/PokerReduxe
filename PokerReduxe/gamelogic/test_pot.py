import unittest


from table import Table
from player import Player
from seat import Seat
from dealer import Dealer


class TestPot(unittest.TestCase):
    """Do we have a fully functional pot object?"""

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

    def test_who_is_first_pre_flop(self):
        """Do we make the proper player act first pre-flop??"""
        self.dealer.deal_hole()
        self.assertTrue(self.table.seats[self.table.under_the_gun].player.action)

    def test_who_is_first_post_flop(self):
        """Do we make the proper player act first post-flop"""
        self.dealer.deal_hole()
        self.table.seats[self.table.under_the_gun].player.action = False
        self.dealer.deal()
        self.assertTrue(self.table.seats[self.table.first].player.action)

    def test_bet(self):
        """Can each player bet 50?"""
        self.dealer.deal_hole()
        i = 0
        while i < 6:
            i += 1
            for seat in self.table.pots[-1].seats:
                if seat.player.action:
                    seat.player.bet(50)
                    self.table.pots[-1].betting_round()
                    break

    def test_betting_round(self):
        """betting round ends when the pot is called to the initial better"""



if __name__ == '__main__':
    unittest.main()
