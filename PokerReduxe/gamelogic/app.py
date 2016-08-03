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


def reset_player_order(table):
    """ Creating the hand list """
    active_players = get_active_players(table)

    # Grab random index
    players_length = len(active_players)
    i = random.randint(0, players_length - 1)
    x = i + 1

    # loop through players, assigning order, until i is reached
    table.player_order = []
    table.player_order.append(i)
    while x != i:
        if x >= players_length:
            if i == 0:
                return table.player_order
            x = 0
        table.player_order.append(x)
        x += 1
    return table.player_order

def get_active_players(table):
    active_players = []
    for player in table.seats.values():
        if player.active == True:
            active_players.append(player)
    return active_players
