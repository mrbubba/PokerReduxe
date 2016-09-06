from player import Player

class Table(object):
    """
    Table holds the intermediate data needed for the app to drive the game

    ATTRIBUTES:

        @property {str} table_name A name of table
        @property {dict} seats A dict of Player obj representing seat order
        @property {int} sb_amount The small blind amount
        @property {int} bb_amount The big blind amount
        @property {int} ante The ante amount
        @property {list} buy_in A list of two values, min/max buy in
        @property {list} deck A list of strings representing cards
        @property {list} pots A list of pot objects
        @property {list} last_order A list of the last betting order
        @property {list} player_order A list of the current betting order sb first
        @property {list} community_cards A list containing card names
        @property {int} bet_increment The minimum amount the bet can be raised
        @property {int} current_bet Amount to call


    METHODS:

        @method _build_seats Creates the seats dict from seats num
        @method join Adds player object to any empty seat in seats dict
        @method quit Removes player from the seats dict
        @method change_seat Changes a players seat appropriately

    """

    def __init__(self, name, seats, sb_amount, bb_amount, buy_in, ante=0):
        self.table_name = name
        self.seats = {}
        # Build seats dictionary
        self._build_seats(seats)

        self.sb_amount = sb_amount
        self.bb_amount = bb_amount
        self.ante = ante
        self.buy_in = buy_in
        self.deck = []
        self.pots = []
        self.last_order = []
        self.player_order = []
        self.community_cards = []
        self.bet_increment = bb_amount
        self.current_bet = 0

    # @param seats The num of seats passed in instantiation
    # @return null
    def _build_seats(self, seats):
        if seats not in range(2, 10):
            raise ValueError("Tables must have between 2 and 9 players.")
        for i in range(1, seats + 1):
            self.seats[i] = None

    # @param key The key of the seat in seats dict.
    # @param player The player object in question
    # @param stack The players initial buy in
    def join(self, key, player_name, stack):
        # if player is in game already, he cant join
        if player in self.seats.values():
            raise ValueError("You can't join the same game twice")

        # set buy in range
        min_buy = self.buy_in[0]
        max_buy = self.buy_in[1] + 1


        # ensure proper buyin
        if stack not in range(min_buy, max_buy):
            raise ValueError('Buy in must be between {} and {}.'.format(min_buy, self.buy_in[1]))

        # ensure seat is empty
        if not self.seats[key]:
            player = Player(player_name, stack)
            self.seats[key] = player
            self.seats[key].stack = stack
            player.table = self
        else:
            raise ValueError("Don't be rude, this seat is taken.")

    # @param player The player object to remove from seats
    def quit(self, player):
        if player.action:
            player.action = False
            player.fold()
        while player.equity:
            player.active = False
        player.stack = 0
        for k, v in self.seats.items():
            if v == player:
                self.seats[k] = None

    def change_seat(self, player, ind):
        """ A player should be allowed to change to an open seat at the same table """
        # Check for seats range
        if ind >= len(self.seats):
            raise Exception("This seat doesn't exist!!")
        # Check if seat is occupied
        if self.seats[ind] is not None:
            raise Exception("This seat is occupied!!")

        stack_save = player.stack
        self.quit(player)
        self.seats[ind] = player
        player.stack = stack_save
        player.active = True
