from gameserver.gamelogic.app import action_time


class Player(object):
    """
    Player object to be assoc with table seats dictionary

    ATTRIBUTES:

            @property {str} name Name of the player
            @property {list} hole_cards List of players hole cards
            @property {list} working_cards Internal list used to create the hand
            @property {list} hand Internal list used to determine hand rank
            @property {int} stack Number of players chips left on table
            @property {bool} active Indicator for active status
            @property {obj} table The table object that hosts this game
            @property {int} equity Amount player has bet in round
            @property {bool} acted Has player acted in betting round
            @property {bool} action Is action currently on player
            @property {bool} folded removes player from the hand
            @property {bool} missed_sb Indicates player missed small blind
            @property {bool} missed_bb Indicates player missed big blind

    METHODS:

            @method {} bet Add bet to equity and sub from stack
            @method {} fold Removes player from all pot objects

     """
    def __init__(self, name, stack):
        self.name = name
        self.hole_cards = []
        self.working_cards = []
        self.hand = []
        self.stack = stack
        self.active = True
        self.table = None
        self.equity = 0
        self.acted = False
        self.action = False
        self.folded = False
        self.missed_sb = False
        self.missed_bb = False

    def bet(self, amount):
        """When a player action is set to true, bet is the method by which
        a player bets calls or checks appropriately."""
        if self.action:
            payload = {}
            #  A player can always go all in no matter the current_bet
            if amount == self.stack:
                pass
            # Do not let people bet negative
            elif amount < 0:
                raise Exception("Bets can not be negative")

            elif amount < self.table.current_bet and self.stack > 0:
                raise Exception("Must match the current bet")

            # Check that bet/raise is at least the minimum
            elif self.table.current_bet < amount < self.table.current_bet + self.table.bet_increment:
                raise Exception("Minimum raise is {}".format(self.table.current_bet + self.table.bet_increment))

            # Do not let players bet more than stack
            if amount > self.stack:
                raise Exception("You can only bet what you have on the table!!")

            # Take bet from stack and move to equity
            self.stack -= amount
            self.equity += amount
            self.acted = True

            # Set players action to False
            self.action = False
            action_time(self, self.table)

    def fold(self):
        """ Set fold attribute to True and action to False """
        self.folded = True
        if self.action:
            self.action = False
            action_time(self, self.table)
