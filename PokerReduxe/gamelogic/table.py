class Table():
    """
    Table holds the intermediate data needed for the app to drive the game

    ATTRIBUTES:

        @property {dict} seats A dict of Player obj representing seat order
        @property {int} sb_amount The small blind amount
        @property {int} bb_amount The big blind amount
        @property {int} ante The ante amount
        @property {list} deck A list of strings representing cards
        @property {list} pots A list of pot objects

    METHODS:

        @method _build_seats Creates the seats dict from seats num


    """

    def __init__(self, seats, sb_amount, bb_amount, ante=0):
        self.seats = {}
        # Build seats dictionary
        self._build_seats(seats)

        self.sb_amount = sb_amount
        self.bb_amount = bb_amount
        self.ante = ante
        self.deck = []
        self.pots = []

    # @param seats The num of seats passed in instantiation
    # @return null
    # TODO:
    def _build_seats(self, seats):
        if seats > 9 or seats < 2:
            Exception(" Seats must be between 2 and 9 ")

        x = 1
        while x <= seats:
            self.seats[x] = ''
            x += 1
