import random


from pot import Pot
from dealer import Dealer


class Table(object):
    """The table object will largely be the top level object

    Attributes:

        community_cards(list):  a list of the cards shared by all players
        seats(list):  list of seats in the game
        small_blind_amount(int):  how much the small blind costs
        big_blind_amount(int):  how much the big blind costs
        ante(int):  how much the ante costs
        button(int):  indicates which seat has the button
        small_blind(int):  indicates which seat has the small blind (sub
                            of seat in self.seats)
        big_blind(int):  indicates which player has the big blind (sub of
                        seat in self.seats)
        under_the_gun(int):  first player to act pre-flop
        pots(list):  a list of all current pots
        dealer(obj):  the dealer object
        bought_button(int): will be the int of the seat that bought the
                            button, that seat will pay the big and little
                            blinds, the blinds won't move for the following
                            hand, and the small blind will be utg.
        first(int):  tells the pot who is first to act post flop.

    Methods:

         init_hand: if its first hand, init_hand randomly assigns button,
                    otherwise, moves button to the next player.  Increments
                    the small_blind and big_blind attributes appropriately.
                    Resets community_cards and pots to [].  Sets all
                    player.hole attributes [].
                    Creates the initial pot object, deducts the
                    blinds and antes and adds them to the pot.pot. Pot
                    inherits the active seats, and button attributes as well
                    as the big_blind_amount as the initial pot.bet_increment
                    value.
    """

    def __init__(self, seats, small_blind_amount, big_blind_amount, ante=0):
        self.community_cards = []
        self.seats = seats
        self.small_blind_amount = small_blind_amount
        self.big_blind_amount = big_blind_amount
        self.ante = ante
        self.button = None
        self.small_blind = None
        self.big_blind = None
        self.under_the_gun = None
        self.pots = []
        self.dealer = Dealer(self)
        self.bought_button = None
        self.first = None

    def _get_active_seats(self):
        for seat in self.seats:
            if seat.active:
                try:
                    active_seat.append(seat)
                except NameError:
                    active_seat = [seat]
        return active_seat

    def set_button(self):
        """At the start of game we need to randomly assign the button
        and blinds to an active seat."""
        self.button = random.randint(1, len(self.seats) - 1)

        # check to make sure we've assigned the button to an active seat
        for seat in self.seats:
            if seat.player:
                seat.player.missed_big_blind = False
                seat.player.missed_small_blind = False

        move = True
        while move:
            if self.button >= len(self.seats):
                self.button = 0
            if self.seats[self.button].active:
                move = False
            else:
                self.button += 1

        # set the small blind
        self.small_blind = self.button + 1
        move = True
        while move:
            if self.small_blind >= len(self.seats):
                self.small_blind = 0
            if self.seats[self.small_blind].active:
                move = False
            elif self.seats[self.small_blind].player:
                self.seats[self.small_blind].player.missed_small_blind = True
            if move:
                self.small_blind += 1

        # set the big blind
        self.big_blind = self.small_blind + 1
        move = True
        while move:
            if self.big_blind >= len(self.seats):
                self.big_blind = 0
            if self.seats[self.big_blind].active:
                move = False
            elif self.seats[self.big_blind].player:
                self.seats[self.big_blind].player.missed_big_blind = True
            if move:
                self.big_blind += 1

        # set utg (Under the Gun) for first round of betting (first to act)
        self.under_the_gun = self.big_blind + 1
        move = True
        while move:
            if self.under_the_gun >= len(self.seats):
                self.under_the_gun = 0
            if self.seats[self.under_the_gun].active:
                move = False
            else:
                self.under_the_gun += 1

        # reset the blinds appropriately for head to head play
        active = self._get_active_seats()
        if len(active) == 2:
            self.big_blind = self.small_blind
            self.small_blind = self.button
            self.first = self.big_blind
            self.under_the_gun = self.button

    def _reset_blinds(self):
        """ handles corner cases where a missed blind changes the position of
        the blinds"""
        # if someone between small blind and the button goes active they bought
        # the blind

        count = self.button + 1
        self.bought_button = None
        while count != self.small_blind:
            if count >= len(self.seats):
                count = 0
            if count == self.small_blind:
                pass
            elif self.seats[count].active and count:
                if self.bought_button is None:
                    self.bought_button = count
                    self.seats[count].player.missed_small_blind = False
                    self.seats[count].player.missed_big_blind = False
                    count += 1
                else:
                    # only one player can buy the button at a time
                    self.seats[count].active = False
                    self.seats[count].player.frozen = True
                    count += 1
            else:
                count += 1

        # the earliest active seat between the small and big becomes the big blind
        count = self.small_blind + 1
        while count != self.big_blind:
            if count >= len(self.seats):
                count = 0
            if count == self.big_blind:
                pass
            elif self.seats[count].active:
                self.big_blind = count
            else:
                count += 1

    def _button_move(self):
        """moves the buttons and the blinds, clockwise.  Ensures that every
        player pays the blinds for any orbit they are active in."""
        # exits game when down to a single player
        self.seats_active = len(self._get_active_seats())
        if self.seats_active == 1:
            quit()
            # WARNING: quit is simply a pass. maybe what you want to do here is
            # raise a custom exception?

        # correctly sets the small blind/button for head to head play
        # QUESTION: is there a way to refactor this with the code starting at 119?
        elif self.seats_active == 2:
            move = True
            while move:
                self.big_blind += 1
                if self.big_blind >= len(self.seats):
                    self.big_blind = 0
                if self.seats[self.big_blind].active:
                    self.first = self.big_blind
                    move = False
            move = True
            while move:
                self.button += 1
                if self.button == self.big_blind:
                    self.button += 1
                if self.button >= len(self.seats):
                    self.button = 0
                if self.seats[self.button].active:
                    self.small_blind = self.button
                    self.under_the_gun = self.button
                    move = False

        # if one or more players join on a head to head game reset the button
        elif self.seats_active > 2 and self.button == self.small_blind:
            self.set_button()

        # if someone bought the button we must set them to the button
        # but not move the blinds
        elif self.bought_button:
            self.button = self.bought_button
            self.bought_button = None
            self.first = self.small_blind

            #only move the big blind if they busted out last hand
            if not self.seats[self.big_blind].active:
                self.seats[self.big_blind].player.missed_big_blind = True
                move = True
                while move:
                    self.big_blind += 1
                    if self.big_blind >= len(self.seats):
                        self.big_blind = 0
                    if self.seats[self.big_blind].active:
                        move = false
                    else:
                        self.seats[self.big_blind].missed_big_blind = True
            self.under_the_gun = self.big_blind + 1
            move = True
            while move:
                if self.under_the_gun >= len(self.seats):
                    self.under_the_gun = 0
                if self.seats[self.under_the_gun].active:
                    move = False
                else:
                    self.under_the_gun += 1

        else:
            # ensures the button moves to the small blind
            self.button = self.small_blind
            if self.seats[self.button].player:
                button_player = self.seats[self.button].player
            # can't play the button unless you're paid up(no missed blinds)
            if button_player.missed_small_blind or button_player.missed_big_blind:
                button_player.frozen = True
                self.seats[self.button].active = False

            # ensures that the small blind is moved to the appropriate seat
            move = True
            self.small_blind += 1
            while move:
                # resets small_blind to 0 if it is greater than seats
                if self.small_blind >= len(self.seats):
                    self.small_blind = 0
                # if seat is active ends the loop
                if self.seats[self.small_blind].active:
                    move = False
                # if the big blind got stacked there is a dead small blind
                elif self.small_blind == self.big_blind:
                    self.seats[self.small_blind].player.missed_small_blind = True
                    move = False
                else:
                    self.seats[self.small_blind].player.missed_small_blind = True
                    self.small_blind += 1
            # first is first to act post flop
            self.first = self.small_blind

            # ensures that the big blind is moved to the next active seat
            move = True
            self.big_blind += 1
            while move:
                if self.big_blind >= len(self.seats):
                    self.big_blind = 0
                # if seat is active ends the loop
                if self.seats[self.big_blind].active:
                    self.seats[self.big_blind].missed_big_blind = False
                    self.seats[self.big_blind].missed_small_blind = False
                    move = False
                elif self.seats[self.big_blind].player:
                    self.seats[self.big_blind].player.missed_big_blind = True
                    self.seats[self.big_blind].player.missed_small_blind = False
                    self.big_blind += 1
                else:
                    self.big_blind += 1

            self._reset_blinds()

            # if someone bought the button
            if self.bought_button:
                self.first = self.bought_button
                self.under_the_gun = self.small_blind
            else:
                # properly set utg
                move = True
                self.under_the_gun = self.big_blind + 1
                while move:
                    # resets under_the_gun to 0 if it is greater than seats
                    if self.under_the_gun >= len(self.seats):
                        self.under_the_gun = 0
                    # if seat is active ends the loop
                    if self.seats[self.under_the_gun].active:
                        move = False
                    else:
                        self.under_the_gun += 1

    def _create_pot(self):
        """creates the initial pot object with the blinds and antes"""
        # import pdb
        # pdb.set_trace()
        bb = self.seats[self.big_blind]
        sb = self.seats[self.small_blind]
        # as per conversation with Jared this is unneeded all_in = []
        pot = 0
        active_seats = self._get_active_seats()

        # if someone bought the button they post and the blinds don't pay
        if self.bought_button:
            buyer = self.seats[self.bought_button]
            buyer.player.missed_small_blind = False
            buyer.player.missed_big_blind = False

            if buyer.player.stack > self.small_blind_amount + self.big_blind_amount:
                buyer.player.equity = self.big_blind
                buyer.player.stack -= self.small_blind_amount + self.big_blind_amount

            elif buyer.player.stack >= self.big_blind_amount:
                buyer.player.equity = self.big_blind
                buyer.player.stack = 0
        else:
            if sb.active:

                # if big blind was missed post it
                if sb.player.missed_big_blind:

                    if sb.player.stack > self.small_blind_amount + self.big_blind_amount:
                        sb.player.stack -= self.small_blind_amount + self.big_blind_amount
                        sb.player.equity = self.big_blind_amount
                        sb.player.missed_big_blind = False

                    elif sb.player.stack > self.big_blind_amount:
                        sb.player.stack = 0
                        sb.player.equity = self.big_blind_amount
                        sb.player.missed_big_blind = False

                    else:
                        sb.player.equity = sb.player.stack
                        sb.player.stack = 0
                        sb.player.missed_big_blind = False

                elif sb.player.stack > self.small_blind_amount:
                    sb.player.stack -= self.small_blind_amount
                    sb.player.equity = self.small_blind_amount

                # if small blind puts player all in put player in all_in list
                else:
                    sb.player.equity = sb.player.stack
                    sb.player.stack = 0

            # add the big blind to the pot
            if bb.player.stack > self.big_blind_amount:
                bb.player.stack -= self.big_blind_amount
                bb.player.equity = self.big_blind_amount
                bb.player.missed_big_blind = False
                bb.player.missed_small_blind = False

            # if big blind puts player all in put player in all_in list
            elif bb.player.stack <= self.big_blind_amount:
                bb.player.equity = bb.player.stack
                bb.player.stack = 0
                bb.player.missed_big_blind = False
                bb.player.missed_small_blind = False

        # collect missing blinds from active seats
        for seat in active_seats:
            if seat.player.missed_big_blind:
                if seat.player.stack > self.big_blind:
                    seat.player.missed_big_blind = False
                    seat.player.stack -= self.big_blind_amount
                    seat.player.equity = self.big_blind_amount
                else:
                    # if bb puts player all in set equity accordingly
                    # and set missed blinds to False
                    seat.player.equity = seat.player.stack
                    seat.player.stack = 0
                    seat.active = False
                    seat.player.missed_small_blind = False
                    seat.player.missed_big_blind = False

            # rinse wash and repeat with missed small blinds
            if seat.player.missed_small_blind:
                if seat.player.stack > self.small_blind_amount:
                    seat.player.missed_small_blind = False
                    seat.player.stack -= self.small_blind_amount
                    # pre-deal equity cannot exceed bb amount
                    if seat.player.equity == 0:
                        seat.player.equity = self.small_blind_amount
                else:
                    # if sb puts player all in set equity accordingly
                    # and set missed sb to False
                    if seat.player.equity == 0:
                        seat.player.equity = seat.player.stack
                    seat.player.stack = 0
                    seat.player.missed_small_blind = False

        # if there is an ante add it too the pot
        if self.ante > 0:
            for seat in active_seats:
                if seat.player.stack >= self.ante:
                    seat.player.stack -= self.ante
                else:
                    seat.player.stack = 0

        # (pot, init_increment, increment, seats, bet, utg, first, table)
        seats = self._get_active_seats()

        pot = Pot(pot, self.big_blind_amount, self.big_blind_amount, seats,
                  self.big_blind_amount, self.under_the_gun, self.first, self)

        self.pots.append(pot)
        return self.pots

    def _reset_players(self):
        # set player attributes for start of new hand
        self.community_cards = []
        self.pots = []
        for seat in self.seats:
            if seat.player.frozen:
                seat.active = True
                seat.player.frozen = False
            if seat.player is not None:
                seat.player.fold = False
                seat.player.hole = []
                seat.player.hand = []
                seat.player.equity = 0

    def _remove_0_stack(self):
        """set seat to inactive for broke players"""
        for seat in self.seats:
            if seat.active and seat.player.stack == 0:
                seat.active = False

    def init_hand(self):
        """sets the table and players up for a new hand, creates a new pot,
        then calls the dealer """

        self._reset_players()
        self._remove_0_stack()
        if not self.button:
            self.set_button()
        self._button_move()
        self._create_pot()
        self.dealer.deal_hole()
