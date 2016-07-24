from madehand import HandUnit


class Player(Object):
    """The player object
    Attributes:

        name(str):  players name
        stack(int):  players current chip stack
        hole(list):  a list that holds the two private cards for the player
        equity(int):  how much the current player has put in the current round
                      of betting
        table(obj);  the table object
        missed_big_blind(bool): true if the player was inactive for the last
                                big blind
        missed_small_blind(bool): true if the player was inactive for the last
                                  small blind
        frozen(bool):  true if player is active, owes blind/s and is ineligible
                       to play this hand(Player will be inactive for the hand.)
        hot_seat(bool): indicates that action is on the player

        hand(str): the final poker hand as set by Analyzer


    Methods:

        fold:   Removes player from all open pots(ends action for this hand),
                and sets self.action to false
        check:  Only available if pot.current_bet is 0, passes tells table to
                pass action, and sets self.action to false
        call:   transfers money from self.stack to the current pot = to the
                current_bet and sets self.action to false
        bet:    transfers money from self.stack to the current pot.  Must be
                >= pot.current_bet + pot.bet_increment.  Unless the player is
                all in for a lesser amount and sets self.action to false
        play:  Toggle seat.active to True or False
        change_seat:  Change to another available seat
        act(bool):  sets hot_seat, and allows player to act.

    """

    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hole = []
        self.equity = int()
        self.action = False
        self.table = None
        self.missed_big_blind = False
        self.missed_small_blind = False
        self.frozen = False
        self.seat = None
        self.hand = []
        self.handunit = HandUnit()

    # Allows player to sit in or out of a hand.  If player is in a hand they fold
    # They will rejoin on the next hand
    def play(self):
        """allows player to set his seat to active or inactive"""
        if self.seat.active:
            self.seat.active = False
        else:
            self.frozen = True

    def bet(self, amount):
        if self.action:
            self.stack -= amount
            self.equity += amount
            self.table.pots[-1].pot += amount


    def change_seat(self):
        pass
