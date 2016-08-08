class Player(object):
    """
    Player object to be assoc with table seats dictionary

    ATTRIBUTES:

            @property {str} name Name of the player
            @property {list} hole_cards List of players hole cards
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
    def __init__(self, name):
        self.name = name
        self.hole_cards = []
        self.stack = 0
        self.active = True
        self.table = None
        self.equity = 0
        self.acted = False
        self.action = False
        self.missed_sb = False
        self.missed_bb = False
