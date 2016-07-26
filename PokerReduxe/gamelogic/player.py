from madehand import HandUnit


class Player(Object):
    """The player object
    Attributes:

        name(str):  players name
        stack(int):  players current chip stack
        hole(list):  a list that holds the two private cards for the player
        equity(int):  how much the current player has put in the current round
                      of betting
        action(bool): set by the pot to indicate players turn to act
        table(obj);  the table object
        missed_big_blind(bool): true if the player was inactive for the last
                                big blind
        missed_small_blind(bool): true if the player was inactive for the last
                                  small blind
        frozen(bool):  true if player is active, owes blind/s and is ineligible
                       to play this hand(Player will be inactive for the hand.)
        hand(str): the final poker hand as set by Analyzer
        all_in(bool):


    Methods:

        bet:        a players only action, where a bet is an int of
                    -1 is a fold, 0 is check,
                    and 1+ is a bet, appropriate betting logic will be applied on
                    front end client.
                    deducts from player.stack .  Must be == pot.current_bet or
                    >= pot.current_bet + pot.bet_increment.  Unless the player is
                    all in for a lesser amount

        play:       Toggle seat.active to True or False

    """

    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hole = []
        self.equity = int()
        self.action = False
        self.missed_big_blind = False
        self.missed_small_blind = False
        self.frozen = False
        self.seat = None
        self.hand = []
        self.all_in = False

    # Allows player to sit in or out of a hand.  If player is in a hand they fold
    # They will rejoin on the next hand
    def play(self):
        """allows player to set his seat to active or inactive"""
        if self.seat.active:
            self.seat.active = False
        else:
            self.frozen = True

    def bet(self, amount):
        if not self.action:
            pass
        else:
            self.stack -= amount
            self.equity += amount
            if self.stack == 0:
                self.all_in = True
            self.seat.table.pots[-1].betting_round()
