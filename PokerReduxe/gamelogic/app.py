import random

from PokerReduxe.gamelogic.analyze import analyze
from PokerReduxe.gamelogic.card import Card
from PokerReduxe.gamelogic.pot import Pot
# from PokerReduxe.gamelogic.lobby import LobbyInstance

def get_active_players(table):
    active_players = []
    for player in table.seats.values():
        # Check for Zero chips in player stack
        if player.stack == 0:
            player.active = False
        if player.active:
            active_players.append(player)
    return active_players


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
            for k, v in table.seats.items():
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


def new_hand(table):
    # Helper function to facilitate new hand

    active_players = get_active_players(table)

    # Make sure we have at least 2 players
    # while len(active_players) < 2:
    #     active_players = get_active_players(table)

    # TODO:Include a way to remove game from lobby. Ends Game.

    # determine if move or set button
    #if len(active_players) == 1:
    #   return LobbyInstance.idle_tables.append(table)
    # set button if going from head to head to 3 or more
    if len(active_players) > 2 and len(table.player_order) == 2:
        set_button(table)
    # move button for head to head
    elif len(active_players) == 2 and len(table.player_order) == 2:
        move = True
        for player in active_players:
            if player not in table.player_order:
                move = False
        if move:
            move_button(table)
        else:
            set_button(table)
    # set button if going from 3 or more to head to head
    elif len(active_players) == 2 and len(table.player_order) > 2:
        set_button(table)
    # move button if there is more than 2 players and a last order was set
    elif table.player_order:
        move_button(table)
    else:
        set_button(table)


# @param table The table obj to set player_order
def set_button(table):
    """ Creating the hand list """
    active_players = get_active_players(table)
    table.bb_seat = None

    for k, v in table.seats.items():
        v.missed_sb = False
        v.missed_bb = False

    # Grab random index
    players_length = len(active_players)
    i = random.randint(0, players_length - 1)
    x = i + 1

    # loop through players, assigning order, until i is reached
    table.player_order = []
    ind_order = [i]
    while x != i:
        if x >= players_length:
            if i == 0:
                break
            x = 0
        ind_order.append(x)
        x += 1
    for ind in ind_order:
        table.player_order.append(active_players[ind])

    button = 0
    sb = 0
    bb = 0
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

    collect_blinds(table)
    create_initial_pot(table)
    deal_hole(table)

    return table.player_order


def move_button(table):
    """setting the table"""
    table.last_order = table.player_order[:]

    active_players = get_active_players(table)

    #  We need to establish the new playing order
    if not table.player_order[0]:
        table.player_order.pop(0)
        for player in table.player_order:
            if player not in active_players:
                table.player_order.remove(player)
        for player in active_players:
            if player not in table.player_order:
                for k, v in table.seats.items():
                    if v == player:
                        last_seat = k - 1
                        if last_seat < 1:
                            last_seat = len(table.seats)
                seated = False
                while not seated:
                    if table.seats[last_seat] and table.seats[last_seat]in table.player_order:
                        my_seat = table.player_order.index(table.seats[last_seat] + 1)
                        table.player_order.insert(my_seat, player)
                        seated = True
                    else:
                        last_seat -= 1
                        if last_seat < 1:
                            last_seat = len(table.seats)

    else:
        for player in table.player_order:
            if player not in active_players:
                table.player_order.remove(player)
        for player in active_players:
            if player not in table.player_order:
                for k, v in table.seats.items():
                    if v == player:
                        last_seat = k - 1
                        if last_seat < 1:
                            last_seat = len(table.seats)
                seated = False
                while not seated:
                    if table.seats[last_seat] and table.seats[last_seat]in table.player_order:
                        my_seat = table.player_order.index(table.seats[last_seat]) + 1
                        table.player_order.insert(my_seat, player)
                        seated = True
        if table.last_order[0] and table.last_order[0] in table.player_order:
            table.player_order.append(table.player_order.pop(0))

    # deal with head to head cases
    if len(active_players) == 2:
        table.player_order.append(table.player_order.pop(0))
    else:
        #  We need to set missed big blinds appropriately
        # we need the seat ints of both the last and current bb to determine missed bb
        if not table.bb_seat:
            for k, v in table.seats.items():
                if v == table.last_order[1]:
                    table.bb_seat = k
                if v == table.last_order[0]:
                     table.sb_seat = k
        inc = table.bb_seat + 1
        if inc > len(table.seats):
            inc = 1
        for k, v in table.seats.items():
            if v == table.player_order[1]:
                new_bb = k
        while inc is not new_bb:
            if table.seats[inc]:
                table.seats[inc].missed_bb = True
            inc += 1
            if inc > len(table.seats):
                inc = 1
        # now we need to check for a dead small blind
        if not table.seats[table.bb_seat] or not table.seats[table.bb_seat].active:
            table.player_order.insert(0, None)
        # now we have to find the missed small blinds
        inc = table.sb_seat + 1
        if inc > len(table.seats):
            inc = 1
        while inc is not table.bb_seat:
            if table.seats[inc] and table.seats[inc] in table.last_order:
                table.seats[inc].missed_sb = True
        # set bought button and exclude players appropriately
        if table.seats[table.bb_seat] and not table.seats[table.bb_seat].active:
            table.seats[table.bb_seat].missed_sb = True
        if table.player_order[0] and table.player_order[0].missed_bb:
            table.bought_button = True
            while table.player_order[1].missed_bb:
                table.player_order.pop(1)

        # we appropriately set the sb and bb seats attributes for the next hand
        # table.sb_seat = table.bb_seat
        # table.bb_seat = new_bb

        #  If you weren't small blind last turn, you can't be button this turn.
        if table.last_order[0] and table.last_order[0] in table.player_order:
            while table.player_order[-1] is not table.last_order[0]:
                table.player_order[-1].missed_sb = True
                table.player_order.pop()
        while table.player_order[-1].missed_sb or table.player_order[-1].missed_bb:
            table.player_order.pop()

    collect_blinds(table)
    collect_missed_blinds(table)
    create_initial_pot(table)
    set_player_table_attributes(table)
    create_deck(table)
    deal_hole(table)


def collect_blinds(table):
    # Check for head to head or bought button
    # Else normal order
    if len(table.player_order) == 2:
        sb = table.player_order[1]
        bb = table.player_order[0]
    elif table.bought_button:
        sb = table.player_order[0]
        bb = table.player_order[0]
    else:
        sb = table.player_order[0]
        bb = table.player_order[1]

    if table.bought_button:
        if bb.stack >= table.bb_amount + table.sb_amount:
            bb.equity = table.bb_amount + table.sb_amount
            bb.stack -= table.bb_amount + table.sb_amount
        else:
            bb.equity = bb.stack
            bb.stack = 0
    else:
        # Collect the big blind
        if not table.bought_button and bb.stack >= table.bb_amount:
            bb.equity = table.bb_amount
            bb.stack -= table.bb_amount
        elif not table.bought_button:
            bb.equity = bb.stack
            bb.stack = 0

        if sb is not None and not table.bought_button:
            # Collect the small blind
            if sb.stack >= table.sb_amount:
                sb.equity += table.sb_amount
                sb.stack -= table.sb_amount
            else:
                sb.equity += sb.stack
                sb.stack = 0
        # set missed blinds to False
    bb.missed_bb = False
    if sb:
        sb.missed_sb = False


def collect_missed_blinds(table):
    for player in table.player_order:
        if player and player.missed_bb:
            if player.stack >= table.bb_amount:
                player.equity += table.bb_amount
                player.stack -= table.bb_amount
            else:
                player.equity = player.stack
                player.stack = 0
            player.missed_bb = False

        if player and player.missed_sb:
            if player.stack >= table.sb_amount:
                player.equity += table.sb_amount
                player.stack -= table.sb_amount
            else:
                player.equity += player.stack
                player.stack = 0
            player.missed_sb = False


def create_initial_pot(table):
    amount = 0
    side_pots = []
    # if there are antes take them
    if table.ante > 0:
        for player in table.player_order:
            if player.stack > table.ante:
                player.stack -= table.ante
                player.equity += table.ante
            else:
                player.equity += player.stack
                player.stack = 0
    # set correct equities and add side pots as necessary
    for player in table.player_order:
        if player and player.equity >= table.ante:
            amount += table.ante
            player.equity -= table.ante
        elif player:
            amount += player.equity
            player.equity = 0
            side_pots.append(0)
        if player and player.equity > table.bb_amount:
            amount += player.equity - table.bb_amount
            player.equity = table.bb_amount
        if player and not player.stack:
            side_pots.append(player.equity)

    # instantiate pot object
    players = table.player_order[:]
    pot = Pot(players, amount)
    # add the side_pots list
    pot.side_pots = side_pots

    # Add the initial pot to the table
    table.pots.append(pot)


def set_player_table_attributes(table):
    """ Resets players hole card and acted attributes and community_cards """

    table.community_cards = []

    for player in table.player_order:
        if player:
            player.hand = []
            player.working_cards = []
            player.hole_cards = []
            player.acted = False
            player.folded = False


def create_deck(table):
    """ Creates a randomized deck """
    # Make a standard poker deck (14 represents an ace)

    for value in range(2, 15):

        if value > 10:
            if value == 11:
                name = 'Jack'
            elif value == 12:
                name = 'Queen'
            elif value == 13:
                name = 'King'
            elif value == 14:
                name = 'Ace'
        else:
            name = str(value)

        table.deck.append(Card(name + "_Diamonds", value, "d"))
        table.deck.append(Card(name + "_Hearts", value, "h"))
        table.deck.append(Card(name + "_Spades", value, "s"))
        table.deck.append(Card(name + "_Clubs", value, "c"))

    random.shuffle(table.deck)


def deal_hole(table):
    """ Deals 2 hole cards to each player in hand """
    set_player_table_attributes(table)
    create_deck(table)

    for player in table.player_order:
        if player:
            player.hole_cards.append(table.deck.pop(0))
            player.hole_cards.append(table.deck.pop(0))

    inc = 2
    # Set Inc for head to head
    if len(table.player_order) == 2 or table.bought_button:
        inc = 1
    table.bought_button = False
    player = table.pots[-1].players[inc]
    table.current_bet = table.bb_amount
    action_time(player, table)


def _action_engine(table, inc):
    pot = table.pots[-1]
    if pot.players[inc].folded:
        return action_time(pot.players[inc], table)
    if pot.players[inc].stack == 0:
        inc += 1
        if inc == len(pot.players):
            inc = 0
        _action_engine(table, inc)
    elif pot.players[inc].acted and pot.players[inc].equity == table.current_bet:
        evaluate_pot(table)
    else:
        pot.players[inc].action = True


def action_time(player, table):
    pot = table.pots[-1]
    inc = pot.players.index(player)
    # list comprehension to check for all in players, break if so
    current_players = [x for x in pot.players if x and x.stack > 0]
    if len(current_players) < 2:
        return evaluate_pot(table)
    inc += 1
    if inc == len(pot.players):
        inc = 0
    if player.folded:
        next_player = pot.players[inc]
        player.folded = False
        for pot in table.pots:
            pot.players.remove(player)
        inc = pot.players.index(next_player)
        return _action_engine(table, inc)
    if player.equity > table.current_bet + table.bet_increment:
        table.bet_increment = player.equity - table.current_bet
    if player.equity > table.current_bet:
        table.current_bet = player.equity
    if player.stack == 0:
        if player.equity not in pot.side_pots:
            pot.side_pots.append(player.equity)
    if pot.players[inc].folded:
        player = pot.players[inc]
        return action_time(player, table)
    if pot.players[inc].stack == 0:
        player = pot.players[inc]
        return action_time(player, table)
    return _action_engine(table, inc)


def evaluate_pot(table):
    """ Evaluates pot on table and creates side pots if necessary """
    pot = table.pots[-1]
    if pot.side_pots:
        pot.side_pots = sorted(pot.side_pots)
        while pot.side_pots:
            amount = pot.side_pots.pop(0)

            x = 0
            new_players = []
            for player in pot.players:
                player.equity -= amount
                x += 1
                new_players.append(player)

            for player in pot.players:
                if player.stack == 0 and player.equity == 0:
                    pot.players.remove(player)
            for p in pot.side_pots:
                ind = pot.side_pots.index(p)
                pot.side_pots[ind] -= amount

            amount = amount * x
            amount += pot.amount
            pot.amount = 0
            new_pot = Pot(new_players, amount)
            table.pots.insert(0, new_pot)

            if len(pot.players) == 1:
                pot.side_pots = []

    for player in pot.players:
        pot.amount += player.equity
        player.equity = 0

    if len(pot.players) == 1:
        # Give last guy in pot money
        pot.players[0].stack += pot.amount
        table.pots.pop()

        if not table.pots:

            # Start new hand
            new_hand(table)
        else:
            while len(table.community_cards) < 5:
                deal(table)
            analyze(table)
            new_hand(table)
    else:
        for player in pot.players:
            player.acted = False
        if len(table.community_cards) < 5:
            deal(table)
        else:
            analyze(table)
            new_hand(table)


def deal(table):
    table.current_bet = 0
    if len(table.community_cards) == 0:
        for x in range(0, 3):
            table.community_cards.append(table.deck.pop(0))
    else:
        table.community_cards.append(table.deck.pop(0))
    action_time(table.pots[-1].players[-1], table)
