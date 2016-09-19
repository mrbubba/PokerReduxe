import json

from PokerReduxe.gamelogic.lobby import LobbyInstance


def handler_response(table):
    if table.player_order:
        action_player = [player for player in table.player_order if player.action]
        action_player = action_player[0].name
        first_player = table.player_order[0].name
    else:
        action_player = None
        first_player = None

    players = {}
    for key, value in table.seats.items():
        if value is not None:
            players[value.name] = [key, value.stack, value.equity, value.folded, value.active,
                                   value.hole_cards[0].name, value.hole_cards[1].name]
    pots = []
    if table.pots:
        pot_players = []
        for pot in table.pots:
            amount = pot.amount
            for player in pot.players:
                pot_players.append(player.name)
            pots.append([amount, pot_players[:]])
            pot_players = []
    com_cards = []
    if table.community_cards:
        for card in table.community_cards:
            com_cards.append(card.name)
    payload = {"table": table.table_name,
               "table_stats": [len(table.seats), table.sb_amount, table.bb_amount, table.buy_in, table.ante,
                               com_cards, action_player, first_player], "players": players,
               "pots": pots}
    payload = json.dumps(payload)

    return payload


def handler(data):
    """takes the data json object from the socket, makes the python calls to the game server,
    and returns the payload json object to the socket"""
    data = json.loads(data.decode("utf-8"))
    d_item = data["item"]
    d_action = data["action"]
    d_data = data["data"]

    if d_item == "LOBBY":
        if d_action == "get_lobby":
            payload = {}
            payload["tables"] = {}
            if LobbyInstance.tables:
                for table in LobbyInstance.tables:
                    num_players = 0
                    for v in table.seats:
                        if table.seats[v] is not None:
                            num_players += 1
                    payload_item = [num_players, len(table.seats), table.sb_amount,
                                    table.bb_amount, table.ante, table.buy_in]
                    payload["tables"][table.table_name] = payload_item
            payload = json.dumps(payload)
            return payload
        elif d_action == "create_table":
            LobbyInstance.create_table(d_data[0], d_data[1], d_data[2], d_data[3], d_data[4], d_data[5], d_data[6],
                                       d_data[7])
            return d_data[2]

    table = [table for table in LobbyInstance.tables if table.table_name == d_data[0]]
    table = table[0]
    for key, value in table.seats.items():
        if value and value.name == d_data[1]:
            player = table.seats[key]
    if d_item == "TABLE":

        if d_action == "change_seat":
            table.change_seat(player, d_data[2])
            return handler_response(table)

        elif d_action == "join_table":
            table.join(d_data[2], d_data[1], d_data[3])
            return handler_response(table)

    elif d_item == "PLAYER":

        if d_action == "bet":
            player.bet(d_data[2])
            return handler_response(table)

        elif d_action == "fold":
            player.fold()
            return handler_response(table)
