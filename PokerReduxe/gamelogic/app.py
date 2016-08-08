import random
from pot import Pot
#
# # @param {obj} table the table to draw info from
# # @return {obj} payload pot, list of players sb first
# def runGame():
#     setupTable(table)
#     pushAction(table.players, table.pot)
#
# def setupTable(table):
#     getPlayerList()  #
#     create_pot()
#     pass
#
# # @param {list} pot A list of pot objects
# # @param {list} activeplayers
# def pushAction(players, pot):
#     if 2 peeps left:
#         # reward winner
#         return Analyzer(players,pot)
#
#     else
#         # remove players and mod pots
#         getactiveplayers
#
#
#
#
#     get_active_players = [x for x in table.seats.players]
#     betting_order = getBettingOrder(table, get_active_players)
#     check_missed_blinds = table.check_missed_blinds(betting_order)
#     betting_order = getBettingOrder(table, check_missed_blinds)
#     button = getButton()
#
#
#     create_side_pot(table, pot)
#
#         return pushAction(table, pot)
#
#
# def create_side_pot(table, pot):
#     side_pots = table.pots[-1].side_pots
#     if side_pots:
#         side_pots = side_pots.order()
#             while side_pots:
#                 players = pot.players[:]
#                 amount = side_pots.pop(0)
#
#
#         create_pot(table, players)
#
# def create_pot(table, players):
#     pot = Pot(table, players)
#     table.pots.append(pot)
#     return


def check_active_players(table):

    # Grab active players at table
    active_players = get_active_players(table)

    # Remove inactive players from table player order
    for player in table.player_order:
        if player not in active_players:
            table.player_order.remove(player)

    # Add active players not in player order appropriately
    for player in active_players:
        if player not in table.player_order:
            ind_order = []
            # If active player not in player_order, collect seat num of every
            # active player
            for k, v in table.seats.items():
                if v.active:
                    ind_order.append(k)
            # Order active seat keys in numerical order
            sorted(ind_order)
            # Finding seat num of first player in player_order
            for k,v in table.seats.items():
                if v == table.player_order[0]:
                    i = k
                    x = i
            # recreate player_order with all active players
            table.player_order = []
            table.player_order.append(table.seats[i])
            i += 1
            while i != x:
                if i in ind_order:
                    table.player_order.append(table.seats[i])
                i += 1
                if i > ind_order[-1]:
                    i = 0


def move_button(table):
    """ Setting the table """

    # Set the last hand order to table
    table.last_order = table.player_order[:]

    # Check for None value remove if present
    if table.player_order[0] is None:
        table.player_order.pop(0)

    # Check active players
    check_active_players(table)

    # Check for MIA BB
    if table.last_order[1] not in table.player_order:
        table.player_order.insert(0, None)
    elif table.last_order[0] is not None:
        # Pop off first value in player order and add to end
        x = table.player_order.pop(0)
        table.player_order.append(x)

    # Check/Set missed bb
    if table.last_order[1] in table.player_order:
        # Grab last bb seat number
        for k,v in table.seats.items():
            if v == table.last_order[1]:
                last_bb_key = k + 1

        # Grab current bb seat number
        for k,v in table.seats.items():
            if v == table.player_order[1]:
                current_bb_key = k

        # Iterate seats between last bb and current bb to missed_bb True
        while last_bb_key != current_bb_key:
            if table.seats[last_bb_key]:
                table.seats[last_bb_key].missed_bb = True
            last_bb_key += 1
            if last_bb_key > len(table.seats):
                last_bb_key = 1


    # Check/Set missed sb
    # if last sb is none, and current sb is none, nobody missed sb
    if table.last_order[0] is not None:
        # Grab last sb seat number
        for k, v in table.seats.items():
            if v == table.last_order[0]:
                last_sb_key = k + 1

        # Grab current sb seat number
        if table.player_order[0] is not None:
            for k, v in table.seats.items():
                if v == table.player_order[0]:
                    current_sb_key = k
        else:
            for k, v in table.seats.items():
                if v == table.player_order[1]:
                    current_sb_key = k

        # Iterate seats between last sb and current sb to missed_sb True
        while last_sb_key != current_sb_key:
            if table.seats[last_sb_key].acted or table.seats[last_sb_key].missed_bb:
                table.seats[last_sb_key].missed_sb = True
            last_sb_key += 1
            if last_sb_key > len(table.seats):
                last_sb_key = 1


# @param table The table obj to set player_order
def reset_player_order(table):
    """ Creating the hand list """
    active_players = get_active_players(table)

    # Grab random index
    players_length = len(active_players)
    i = random.randint(0, players_length - 1)
    x = i + 1

    # loop through players, assigning order, until i is reached
    table.player_order = []
    ind_order = []
    ind_order.append(i)
    while x != i:
        if x >= players_length:
            if i == 0:
                break
            x = 0
        ind_order.append(x)
        x += 1
    for ind in ind_order:
        table.player_order.append(active_players[ind])

    # Have to set missed blind status for inactive players up front
    for k, v in table.seats.items():
        # Grab key of button
        if v == table.player_order[-1]:
            button = k
        # Grab key of sb
        if v == table.player_order[0]:
            sb = k
        # Grab key of bb
        if v == table.player_order[1]:
            bb = k

    # Set missed_sb for immediately inactive players between button and sb
    button += 1
    if button > len(table.seats):
        button = 1
    while button != sb:
        if table.seats[button]:
            table.seats[button].missed_sb = True
        button += 1
        if button > len(table.seats):
            button = 1

    # Set missed_bb for immediately inactive players between sb and bb
    sb += 1
    if sb > len(table.seats):
        sb = 1

    while sb != bb:
        if table.seats[sb]:
            table.seats[sb].missed_bb = True
        sb += 1
        if sb > len(table.seats):
            sb = 1

    return table.player_order


def get_active_players(table):
    active_players = []
    for player in table.seats.values():
        # Check for Zero chips in player stack
        if player.stack == 0:
            player.active = False
        if player.active == True:
            active_players.append(player)
    return active_players


def missed_blind_corner_cases(table):

    # Remove people who missed blinds from button position
    while len(table.player_order) > 2:
        button = table.player_order[-1]
        if button.missed_sb or button.missed_bb:
            table.player_order.remove(button)
        else:
            break

    # Allow bought button
    if table.player_order[0].missed_bb:
        table.player_order[0].missed_bb = False
        table.player_order[0].missed_sb = False
        if table.player_order[0].stack >= table.sb_amount + table.bb_amount:
            table.player_order[0].stack -= table.sb_amount + table.bb_amount
            table.player_order[0].equity += table.sb_amount + table.bb_amount
        else:
            table.player_order[0].equity = table.player_order[0].stack
            table.player_order[0].stack = 0

        x = False
        while x == False:
            # Only one person can buy button at a time
            if table.player_order[1].missed_bb:
                table.player_order.pop(1)
            else:
                x = True


def collect_blinds(table):
    sb = table.player_order[0]
    bb = table.player_order[1]

    # Check for bought button
    if sb is not None and sb.equity > 0:
        return
    if sb is not None:
        # Collect the small blind
        if sb.stack >= table.sb_amount:
            sb.equity += table.sb_amount
            sb.stack -= table.sb_amount
        else:
            sb.equity = sb.stack
            sb.stack = 0
    # Collect the big bling
    if bb.stack >= table.bb_amount:
        bb.equity = table.bb_amount
        bb.stack -= table.bb_amount
    else:
        bb.equity = bb.stack
        bb.stack = 0
    bb.missed_bb = False
    bb.missed_sb = False

def collect_missed_blinds(table):
    for player in table.player_order:
        if player.missed_bb:
            if player.stack >= table.bb_amount:
                player.equity += table.bb_amount
                player.stack -= table.bb_amount
            else:
                player.equity = bb.stack
                player.stack = 0
            player.missed_bb = False

        if player.missed_sb:
            if player.stack >= table.sb_amount:
                player.equity += table.sb_amount
                player.stack -= table.sb_amount
            else:
                player.equity += sb.stack
                player.stack = 0
            player.missed_sb = False

def create_initial_pot(table):

    amount = 0
    side_pots_tmp = []
    if table.ante > 0:
        for player in table.player_order:
            if player.stack > table.ante:
                amount += table.ante
                player.stack -= table.ante
                player.equity += table.ante
            else:
                player.equity = player.stack
                amount += player.stack
                side_pots_tmp.append(player.stack)
                player.stack = 0
            if player.equity > (table.bb_amount + table.ante):
                amount += (player.equity - (table.bb_amount + table.ante))
                player.equity = table.bb_amount + table.ante

    # instantiate pot object
    pot = Pot(table.player_order, amount)

    # append side pots to Pot obj in case of all-in players
    if side_pots_tmp:
        for p in side_pots_tmp:
            pot.side_pots.append(p)

    # Add the initial pot to the table
    table.pots.append(pot)



def set_player_table_attributes(table):
    """ Resets players hole card and acted attributes and community_cards """

    table.community_cards = []

    for player in table.player_order:
        player.hole_cards = []
        player.acted = False

def create_deck(table):
    """ Creats a randomized deck """
    # Make a standard poker deck (14 represents an ace)
    for value in range(2, 15):
        table.deck.append('{}h'.format(value))
        table.deck.append('{}d'.format(value))
        table.deck.append('{}c'.format(value))
        table.deck.append('{}s'.format(value))

    # Shuffle Deck
    random.shuffle(table.deck)

def deal_hole(table):
    """ Deals 2 hole cards to each player in hand """

    create_deck(table)

    for player in table.player_order:
        player.hole_cards.append(table.deck.pop(0))
        player.hole_cards.append(table.deck.pop(0))
