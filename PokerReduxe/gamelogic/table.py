class Table():
    """
    Table holds the intermediate data needed for the app to drive the game

    ATTRIBUTES:

        @property {dict} seats A dict of Player obj representing seat order
        @property {int} sb_amount The small blind amount
        @property {int} bb_amount The big blind amount
        @property {int} ante The ante amount
        @property {list} buy_in A list of two values, min/max buy in
        @property {list} deck A list of strings representing cards
        @property {list} pots A list of pot objects
        @property {list} last_order A list of the last betting order
        @property {list} player_order A list of the current betting order sb first


    METHODS:

        @method _build_seats Creates the seats dict from seats num
        @method join Adds player object to any empty seat in seats dict
        @method quit Removes player from the seats dict
        @method change_seat Changes a players seat appropriately

    """

    def __init__(self, seats, sb_amount, bb_amount, buy_in, ante=0):
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

    # @param seats The num of seats passed in instantiation
    # @return null
    def _build_seats(self, seats):
        if seats not in range(2, 10):
            raise ValueError("Tables must have between 2 and 9 players.")
        for i in range(1,seats + 1):
            self.seats[i] = None

    # @param key The key of the seat in seats dict.
    # @param player The player object in question
    # @param stack The players initial buy in
    def join(self, key, player, stack):
        # if player is in game already, he cant join
        if player in self.seats.values():
            raise ValueError("You can't join the same game twice")

        # set buyin range
        min_buy = self.buy_in[0]
        max_buy = self.buy_in[1] + 1

        # ensure proper buyin
        if stack not in range(min_buy, max_buy):
            raise ValueError('Buy in must be between {} and {}.' .format(min_buy, self.buy_in[1]))

        # ensure seat is empty
        if self.seats[key] == None:
            self.seats[key] = player
            self.seats[key].stack = stack
            self.seats[key].table = self
        else:
            raise ValueError("Don't be rude, this seat is taken.")

    # @param player The player object to remove from seats
    def quit(self, player):
        player.table = None
        player.stack = 0
        for k,v in self.seats.items():
            if v == player:
                self.seats[k] = None

    def change_seat(self):
        pass
