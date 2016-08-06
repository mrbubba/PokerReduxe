class Pot():
    """
    Pot object which contains initial pot, and side pots for a betting round.
    At end of betting round side pots get created.

    ATTRIBUTES:

        @property {list} players A list of player objects in pot
        @property {int} amount Amount of chips in the pot
        @property {list} side_pots


    """
    def __init__(self, players, amount):
        self.players = players
        self.amount = amount
        self.side_pots = []
