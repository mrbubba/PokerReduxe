from .analyzer import Analyzer


class Pot(object):
    """The pot object will drive and track the betting action for each round of
        play.

    Attributes:

        pot(int):   total amount of chips in the middle(another words all chips
                    not currently in player.stack)
        init_increment(int):  bet increment at the start of each betting round
        increment(int):  current bet increment for this round of betting
        seats(list):  list of seats currently in the pot not all in
        bet(int):  the current bet
        utg(int):  position that is first to act preflop
        first(int):  position of first to act after the flop
        table(obj):  the table object


    methods:

        betting_round:  if there is only one player in the hand adds pot.pot
                        to that player.stack, unless there are multiple pots (indicating 1 or more all in players) in which case the
                        remaining community cards are dealt and analyzer is
                        called. otherwise sets the appropriate players action
                        attribute to true to drive the action. betting will be
                        called by dealer to let pot know its time for a round
                        of betting.

        new_pot:  creates a new pot if a player is all in for less then the
                    current bet(if two or more players are in for the higher amount)

    """

    def __init__(self, pot, init_increment, increment, seats, bet, utg, first, table):
        self.pot = pot
        self.init_increment = init_increment
        self.increment = increment
        self.seats = seats
        self.bet = bet
        self.utg = utg
        self.first = first
        self.table = table

    def _new_pot(self):
        # TODO: spawn new pot in case of all in action
        pass

    def betting_round(self):
        """we need a round of betting.  Must appropriately tell players to act,
        create new pot, tell dealer to act, or if all but one player has folded
        award the pot to the remaining player and notify the table to start a
        new hand.
        """
        # are we in the middle of an active round of betting?
        # If so increment to the next active player
        for seat in self.seats:
            # Do we have more than one person left in the hand?
            # if only 1 person left in action, and only 1 pot; award winner
            # and initiate new hand
            if len(self.seats) == 1 and len(self.table.pots) == 1:
                self.seats[0].player.stack += self.pot
                return self.table.init_hand()
            # if only 1 active person left in hand, and multiple pots,
            # we must have all in players
            elif len(self.seats) == 1:
                # deal remaining cards
                while len(self.table.community_cards) < 5:
                    self.table.dealer.deal()
                return Analyzer(self.table)
            # this loop will only happen if already in a betting round
            if seat.player.action:
                seat.player.action = False
                i = self.seats.index(seat)
                i += 1
                if i == len(self.seats):
                    i = 0
                self.seats[i].player.action = True
                if self.bet == 0 and i == self.first:
                    self.table.dealer.deal()
                    return
                elif i == self.utg and self.bet == self.init_increment:
                    self.table.dealer.deal()
                    return
                elif self.bet > self.init_increment and self.bet == self.seats[i].player.equity:
                    self.table.dealer.deal()
                    return
        # Everything below will happen only for the first player in a betting round
        # if no community cards have been dealt utg is first to act
        if not self.table.community_cards:
            self.seats[self.utg].player.action = True
        # if community cards then first is first to act.
        else:
            self.seats[self.first].player.action = True
