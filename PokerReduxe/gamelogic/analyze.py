from table import Table
from pot import Pot


def setup(table):
    """get the players in the pot and their hands"""
    pot = table.pots.pop()
    for player in pot.players:
        player.hole_cards += table.community_cards
    return pot


def order(pot):
    """ order players hands in descending order """
    for player in pot.players:
        player.hole_cards.sort(key=lambda x: x.value, reverse=True)
    return pot


def flush(pot):
    """ Identify flushes """
    for player in pot.players:
        if not player.hand:
            suits = {'d': [], 'h': [], 's': [], 'c': []}
            for card in player.hole_cards:
                x = card.suit
                suits[x].append(card.value)
            for suit in suits:
                if len(suits[suit]) >= 5:
                    player.hole_cards = list(suits[suit])
                    straight(player)
                    if player.hand:
                        value = player.hand[1]
                        player.hand = [8, value]
                    else:
                        while len(player.hole_cards) > 5:
                            player.hole_cards.pop()
                        player.hand = [5] + player.hole_cards
    return pot


def convert_to_card_value(pot):
    """ Convert all hole cards to card values """
    x = []
    for player in pot.players:
        if not player.hand:
            for card in player.hole_cards:
                x.append(card.value)
            player.hole_cards = x[:]
            x = []
            straight(player)
    return pot


def straight(player):
    """ Identifies the highest straight in hand """
    if not player.hand:
        for card in player.hole_cards:
            if card >= 5:
                if card - 1 in player.hole_cards and card - 2 in player.hole_cards and card - 3 in player.hole_cards:
                    if card - 4 in player.hole_cards:
                        player.hand = [4, card]
                        return
                    elif card == 5 and 14 in player.hole_cards:
                        player.hand = [4, card]
                        return


def matching(pot):
    """ identifies the highest value matching hands eg quads to pairs """
    for player in pot.players:
        if not player.hand:
            trips = []
            pairs = []
            for card in player.hole_cards:
                count = player.hole_cards.count(card)
                if count == 4:
                    kicker = [x for x in player.hole_cards if x != card]
                    player.hand = [7, card, kicker[0]]
                    break
                elif count == 3:
                    trips.append(card)
                    player.hole_cards = [x for x in player.hole_cards if x != card]
                elif count == 2:
                    pairs.append(card)
                    player.hole_cards = [x for x in player.hole_cards if x != card]
            if trips:
                if len(trips) == 2:
                    player.hand = [6, trips[0], trips[1]]
                elif pairs:
                    player.hand = [6, trips[0], pairs[0]]
                else:
                    player.hand = [3, trips[0], player.hole_cards[0], player.hole_cards[1]]
            elif pairs:
                if len(pairs) > 1:
                    player.hand = [2, pairs[0], pairs[1], player.hole_cards[0]]
                else:
                    player.hand = [1, pairs[0], player.hole_cards[0], player.hole_cards[1], player.hole_cards[2]]
            elif not player.hand:
                player.hand = [0] + player.hole_cards


def compare(pot):
    """ Compares all player hands and awards pot to the winners """
    pass


def analyze(table):
    """"analyze is called at the end of a hand. It determines who and awards
    each pot to the player/s with the best hand"""
    pass