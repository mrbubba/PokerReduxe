import random

from PokerReduxe.gamelogic.analyze import analyze
from PokerReduxe.gamelogic.pot import Pot
from PokerReduxe.gamelogic.card import Card


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

    # set button if going from head to head to 3 or more
    if len(active_players) > 2 and len(table.player_order) == 2:
        set_button(table)
    # move button for head to head
    elif len(active_players) == 2 and len(table.player_order) == 2:
        move_button(table)
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

    return table.player_order


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
    last_bb_key = None
    if table.last_order[1] in table.player_order:
        # Grab last bb seat number
        for k, v in table.seats.items():
            if v == table.last_order[1]:
                last_bb_key = k + 1

        # Grab current bb seat number
        current_bb_key = None
        for k, v in table.seats.items():
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
        last_sb_key = None
        for k, v in table.seats.items():
            if v == table.last_order[0]:
                last_sb_key = k + 1

        # Grab current sb seat number
        current_sb_key = None
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
        while not x:
            # Only one person can buy button at a time
            if table.player_order[1].missed_bb:
                table.player_order.pop(1)
            else:
                x = True


def collect_blinds(table):
    # Check for head to head
    # Else normal order
    if len(table.player_order) == 2:
        sb = table.player_order[1]
        bb = table.player_order[0]
    else:
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
                player.equity = player.stack
                player.stack = 0
            player.missed_bb = False

        if player.missed_sb:
            if player.stack >= table.sb_amount:
                player.equity += table.sb_amount
                player.stack -= table.sb_amount
            else:
                player.equity += player.stack
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
    players = table.player_order[:]
    pot = Pot(players, amount)

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
        player.hole_cards.append(table.deck.pop(0))
        player.hole_cards.append(table.deck.pop(0))

    inc = 2
    # Set Inc for head to head
    if len(table.player_order) == 2:
        inc = 1
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
    current_players = [x for x in pot.players if x.stack > 0]
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
    else:
        for player in pot.players:
            player.acted = False
        if len(table.community_cards) < 5:
            deal(table)
        else:
            analyze(table)


def deal(table):
    table.current_bet = 0
    if len(table.community_cards) == 0:
        for x in range(0, 3):
            table.community_cards.append(table.deck.pop(0))
    else:
        table.community_cards.append(table.deck.pop(0))
    action_time(table.pots[-1].players[-1], table)
