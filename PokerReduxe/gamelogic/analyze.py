payload = {}
payload['pots'] = []
payload['winners'] = []

def setup(table):
    """get the players in the pot and their hands"""
    pot = table.pots.pop()
    py_pot = {}
    py_pot['players'] = []
    py_pot['amount'] = pot.amount
    for player in pot.players:
        if not player.hand:
            player.working_cards = player.hole_cards[:]
            player.working_cards += table.community_cards
            py_pot['players'].append(player.name)
    payload['pots'].append(py_pot)
    return pot


def order(pot):
    """ order players hands in descending order """
    for player in pot.players:
        if not player.hand:
            player.working_cards.sort(key=lambda x: x.value, reverse=True)
    return pot


def flush(pot):
    """ Identify flushes """
    for player in pot.players:
        if not player.hand:
            suits = {'d': [], 'h': [], 's': [], 'c': []}
            for card in player.working_cards:
                x = card.suit
                suits[x].append(card.value)
            for suit in suits:
                if len(suits[suit]) >= 5:
                    player.working_cards = list(suits[suit])
                    straight(player)
                    if player.hand:
                        value = player.hand[1]
                        player.hand = [8, value]
                    else:
                        while len(player.working_cards) > 5:
                            player.working_cards.pop()
                        player.hand = [5] + player.working_cards
    return pot


def convert_to_card_value(pot):
    """ Convert all hole cards to card values """
    x = []
    for player in pot.players:
        if not player.hand:
            for card in player.working_cards:
                x.append(card.value)
            player.working_cards = x[:]
            x = []
            straight(player)
    return pot


def straight(player):
    """ Identifies the highest straight in hand """
    if not player.hand:
        for card in player.working_cards:
            if card >= 5:
                if card - 1 in player.working_cards and card - 2 in player.working_cards \
                        and card - 3 in player.working_cards:
                    if card - 4 in player.working_cards:
                        player.hand = [4, card]
                        return
                    elif card == 5 and 14 in player.working_cards:
                        player.hand = [4, card]
                        return


def matching(pot):
    """ identifies the highest value matching hands eg quads to pairs """
    for player in pot.players:
        if not player.hand:
            trips = []
            pairs = []
            for card in player.working_cards:
                count = player.working_cards.count(card)
                if count == 4:
                    kicker = [x for x in player.working_cards if x != card]
                    player.hand = [7, card, kicker[0]]
                    break
                elif count == 3:
                    trips.append(card)
                    player.working_cards = [x for x in player.working_cards if x != card]
                elif count == 2:
                    pairs.append(card)
                    player.working_cards = [x for x in player.working_cards if x != card]
            if trips:
                if len(trips) == 2:
                    player.hand = [6, trips[0], trips[1]]
                elif pairs:
                    player.hand = [6, trips[0], pairs[0]]
                else:
                    player.hand = [3, trips[0], player.working_cards[0], player.working_cards[1]]
            elif pairs:
                if len(pairs) > 1:
                    player.hand = [2, pairs[0], pairs[1], player.working_cards[0]]
                else:
                    player.hand = [1, pairs[0], player.working_cards[0], player.working_cards[1],
                                   player.working_cards[2]]
            elif not player.hand:
                player.hand = [0] + player.working_cards


def compare(pot):
    """ Compares all player hands and awards pot to the winners """
    value = []
    # get the first value in players hands
    for player in pot.players:
        value.append(player.hand[0])
    # order the values and return the highest value
    value.sort()
    value = value.pop()
    # get rid of all players with a lower value
    pot.players = [x for x in pot.players if x.hand[0] == value]
    # if we're down to one player we have a winner
    if len(pot.players) == 1:
        return pot
    else:
        # since we're down to hands of equal length get the length of
        # the hand so we can iterate through them in search of a winner
        for i in range(1, len(pot.players[0].hand)):
            value = []
            for player in pot.players:
                value.append(player.hand[i])
            value.sort()
            value = value.pop()
            pot.players = [x for x in pot.players if x.hand[i] == value]
        return pot


def award(pot, sb):
    py_winners = []
    """ Awards the pot to the winners """
    if len(pot.players) == 1:
        pot.players[0].stack += pot.amount
        py_winners.append([pot.players[0].name, pot.amount, pot.players[0].stack])
    else:
        remainder = (pot.amount / sb) % len(pot.players)
        pot.amount -= (remainder * sb)
        for player in pot.players:
            amount = pot.amount / len(pot.players)
            player.stack += amount
            py_winners.append([player.name, amount, player.stack])
        i = 0
        while remainder > 0:
            pot.players[i].stack += sb
            py_winners[i][1] += sb
            py_winners[i][2] += sb
            remainder -= 1
            i += 1
    payload['winners'].append(py_winners)


def analyze(table):
    """"analyze is called at the end of a hand. It determines who and awards
    each pot to the player/s with the best hand"""
    while table.pots:
        pot = setup(table)
        order(pot)
        flush(pot)
        convert_to_card_value(pot)
        matching(pot)
        compare(pot)
        award(pot, table.sb_amount)
    return payload
