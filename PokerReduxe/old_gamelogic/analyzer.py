

class Analyzer(object):
    """ Analyzer object

    Attributes:

       table(obj):  table object
       poker_hands(lst): refers poker hands to numbers eg Pair will = 1

    We will represent the poker hands thusly:
        straight flush: [8, 14] for highest possible and [8,5] for lowest possible
        4 of Kind: ( four 10's w/ ace kicker ) : [ 7,10,14]
        full house: ( queens full of 9's ) : [ 6,12,9]
        flush : ( flush with king, jack, 9, 6 and a 4 ) : [ 5, 13,11,9,6,4 ]
        straight: (nine high): [ 4,9]
        three of a kind: ( three 6's an Ace and a King ) : [ 3,6,14,13]
        two pair: ( 8's and 4's and an ace ) : [ 2,8,4,14]
        pair: ( two 9's, and ace, 10 and a 7 )  : [ 1,9,14,10,7]
        high card : ( jack, ten, nine, eight, five ) : [ 0,11,10,9,8,5]

    Methods:

        analyze:    gets the community cards and list of pots from the dealer,
                    for each pot awards the chips to the winner/s
                    If an all in player wins, analyze will reset that seats
                    active to True
    """

    def __init__(self, table):
        self.table = table
        self.seats = self.table.seats
        # self.pot = self.table.pots.pop()
        self.pot = None

    def _award(self, players):
        """awards the pot to the winner(s)"""
        if len(players) == 1:
            players[0].stack += self.pot.pot
        elif (self.pot.pot/self.table.small_blind_amount) % len(players) == 0:
            for player in players:
                player.stack += self.pot.pot / len(players)
        else:
            # if the pot isn't evenly divisible(in small blind units) subtract
            # out the remainder, and split the remaining pot up equally
            remainder = (self.pot.pot/self.table.small_blind_amount) % len(players)
            self.pot.pot = self.pot.pot - (self.table.small_blind_amount * remainder)
            # hand out the remainder one small blind unit at a time starting
            # with first to act
            for player in players:
                player.stack += self.pot.pot / len(players)
            i = self.table.first
            while remainder > 0:
                if self.table.seats[i].player in players:
                    self.table.seats[i].player.stack += self.table.small_blind_amount
                    remainder -= 1
                i += 1
                if i == len(self.table.seats):
                    i = 0

    def _compare(self, players):
        """compares all player hands and awards pot to the winner/s"""
        value = []
        # get the first value in players hands
        for player in players:
            value.append(player.hand[0])
        # order the values and return the highest value
        value.sort()
        value = value.pop()
        # get rid of all players with a lower value
        players = [x for x in players if x.hand[0] == value]
        # if we're down to one player we have a winner
        if len(players) == 1:
            return players
        else:
            # since we're down to hands of equal length get the length of
            # the hand so we can iterate through them in search of a winner
            for i in range(1, len(players[0].hand)):
                value = []
                for player in players:
                    value.append(player.hand[i])
                value.sort()
                value = value.pop()
                players = [x for x in players if x.hand[i] == value]
                # if we're down to one player we have a winner
                if len(players) == 1:
                    return players
            return players

    def _matching(self, players):
        """identifies the highest value matching hands eg quads to pairs"""
        for player in players:
            quads = []
            trips = []
            pairs = []
            if not player.hand:
                # create a local variable 'values' to more easily handle the
                # hand.  Easier to deal with a list of values rather than a list
                # of objects
                values = []
                for card in player.hole:
                    values.append(card.value)
                # here we add appropriate values to the quads, trips,
                # and or pairs variables
                for v in values:
                    count = values.count(v)
                    if count == 4:
                        quads = [v]
                        values = [x for x in values if x != v]
                    elif count == 3:
                        trips.append(v)
                        values = [x for x in values if x != v]
                    elif count == 2:
                        pairs.append(v)
                        values = [x for x in values if x != v]
                # Now we create hands based on the quads, trips,
                # and pairs lists.
                if quads:
                    player.hand = [7, quads[0], values[0]]
                elif trips:
                    if len(trips) == 2:
                        player.hand = [6, trips[0], trips[1]]
                    elif pairs:
                        player.hand = [6, trips[0], pairs[0]]
                    else:
                        player.hand = [3, trips[0], values[0], values[1]]
                elif pairs:
                    if len(pairs) > 1:
                        player.hand = [2, pairs[0], pairs[1], values[0]]
                    else:
                        player.hand = [1, pairs[0], values[0], values[1], values[2]]
                else:
                    player.hand = [0, values[0], values[1], values[2], values[3], values[4]]

    def _straight(self, player):
        """identifies the highest straight in a hand"""
        # create a local variable 'values' to more easily handle the
        # hand.  Easier to deal with a list of values rather than a list
        # of objects
        values = []
        for card in player.hole:
            values.append(card.value)
        for v in values:
            if v >= 5 and not player.hand:
                if v - 1 in values and v - 2 in values and v - 3 in values:
                    if v - 4 in values:
                        player.hand = [4, v]
                        break
                    elif v == 5 and 14 in values:
                        player.hand = [4, v]
                        break
        return player

    def _flush(self, players):
        """Identify those hands that are flushes"""

        for player in players:
            if not player.hand:
                suits = {'d': [], 'h': [], 's': [], 'c': []}
                for card in player.hole:
                    x = card.suit
                    suits[x].append(card)
                for suit in suits:
                    if len(suits[suit]) >= 5:
                        player.hole = list(suits[suit])
                        self._straight(player)
                        if player.hand:
                            value = player.hand[1]
                            player.hand = [8, value]
                        else:
                            player.hand = [5] + player.hole
                # if we have a flush only accept the top five cards to make a
                # old_poker hand
                if player.hand:
                    while len(player.hand) > 6:
                        player.hand.pop()
                else:
                    self._straight(player)
        return players

    def _order(self, players):
        """order players' hands from highest to lowest"""
        for player in players:
            player.hole.sort(key=lambda x: x.value, reverse=True)
        return players

    def _setup(self):
        """get the players in the pot and their hands"""
        for seat in self.pot.seats:
            if seat.active:
                players.append(seat.player)

        for player in players:
            player.hole += self.table.community_cards

        return players

    def analyze(self):
        while self.table.pots:
            self.pot = self.table.pots.pop()
            players = self._setup()
            self._order(players)
            self._flush(players)
            self._matching(players)
            self._compare(players)
            self._award(players)
