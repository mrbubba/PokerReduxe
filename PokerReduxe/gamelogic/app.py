
# @param {obj} table the table to draw info from
# @return {obj} payload pot, list of players sb first
def runGame():
    setupTable(table)
    pushAction(table.players, table.pot)

def setupTable(table):
    getPlayerList()  #
    create_pot()
    pass

# @param {list} pot A list of pot objects
# @param {list} activeplayers
def pushAction(players, pot):
    if 2 peeps left:
        # reward winner
        return Analyzer(players,pot)

    else
        # remove players and mod pots
        getactiveplayers




    get_active_players = [x for x in table.seats.players]
    betting_order = getBettingOrder(table, get_active_players)
    button = getButton()


    create_side_pot(table, pot)

        return pushAction(table, pot)


def create_side_pot(table, pot):
    side_pots = table.pots[-1].side_pots
    if side_pots:
        side_pots = side_pots.order()
            while side_pots:
                players = pot.players[:]
                amount = side_pots.pop(0)

        
        create_pot(table, players)

def create_pot(table, players):
    pot = Pot(table, players)
    table.pots.append(pot)
    return
