from .app import action_time


class Player(object):
    """
    Player object to be assoc with table seats dictionary

    ATTRIBUTES:

            @property {str} name Name of the player
            @property {list} hole_cards List of players hole cards
            @property {list} hand Internal list used to determine hand rank
            @property {int} stack Number of players chips left on table
            @property {bool} active Indicator for active status
            @property {obj} table The table object that hosts this game
            @property {int} equity Amount player has bet in round
            @property {bool} acted Has player acted in betting round
            @property {bool} action Is action currently on player
            @property {bool} missed_sb Indicates player missed small blind
            @property {bool} missed_bb Indicates player missed big blind

    METHODS:

            @method {} bet Add bet to equity and sub from stack
            @method {} fold Removes player from all pot objects

     """
    def __init__(self, name, stack):
        self.name = name
        self.hole_cards = []
        self.hand = []
        self.stack = stack
        self.active = True
        self.table = None
        self.equity = 0
        self.acted = False
        self.action = False
        self.missed_sb = False
        self.missed_bb = False

    def _call_action(self):
        """ After player has acted, player needs to call action on the next
        player """
        my_ind = self.table.pots[-1].players.index(self)
        ind = my_ind + 1
        if ind == len(self.table.pots[-1].players):
            ind = 0
        action_time(self.table, ind)

    def bet(self, amount):
        """When a player action is set to true, bet is the method by which
        a player bets calls or checks appropriately."""
        if self.action:
            # Do not let people bet negative
            if amount < 0:
                raise Exception("Bets can not be negative")

            # Check for all in bet
            elif amount == self.stack:
                self.table.pots[-1].side_pots.append(amount)

            elif amount < self.table.current_bet:
                raise Exception("Must match the current bet")

            # Check that bet/raise is at least the minimum
            elif self.table.current_bet < amount < self.table.current_bet + self.table.bet_increment:
                raise Exception("Minimum raise is {}".format(self.table.current_bet + self.table.bet_increment))

            # Do not let players bet more than stack
            if amount > self.stack:
                raise Exception("You can only bet what you have on the table!!")

            # Set bet increment correctly
            if amount > (self.table.current_bet + self.table.bet_increment):
                self.table.bet_increment = amount - self.table.current_bet

            # Take bet from stack and move to equity
            self.stack -= amount
            self.equity += amount

            # Set players action to False
            self.action = False
            self._call_action()

    def fold(self):
        """ Fold player and remove from all pots """
        if self.action:
            self.action = False
            self._call_action()

            for pot in self.table.pots:
                pot.players.remove(self)
