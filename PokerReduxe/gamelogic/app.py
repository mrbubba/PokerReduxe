import random
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

    return table.player_order


def get_active_players(table):
    active_players = []
    for player in table.seats.values():
        if player.active == True:
            active_players.append(player)
    return active_players
