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

    METHODS:

        @method _build_seats Creates the seats dict from seats num
        @method join Adds player object to any empty seat in seats dict
        @method quit Removes player from the seats dict


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

    # @param seats The num of seats passed in instantiation
    # @return null
    def _build_seats(self, seats):
            try:
                if seats in range(2, 10):
                    x = 1
                    while x <= seats:
                        self.seats[x] = ''
                        x += 1
            except ValueError:
                print(" Seats must be between 2 and 9 ")

    # @param key The key of the seat in seats dict.
    # @param player The player object in question
    # @param stack The players initial buy in
    def join(self, key, player, stack):
        if player in self.seats.values():
            return 'One seat per customer!'
        try:
            min_buy = self.buy_in[0]
            max_buy = self.buy_in[1] + 1
            if self.seats[key] == '' and stack in range(min_buy, max_buy):
                self.seats[key] = player
                self.seats[key].stack = stack
                self.seats[key].table = self
        except ValueError:
            print("Don't be rude, this seat is taken.")

