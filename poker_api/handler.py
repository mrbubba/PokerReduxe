import json

from PokerReduxe.gamelogic.lobby import LobbyInstance


def handler(data):
    """takes the data json object from the socket, makes the python calls to the game server,
    and returns the payload json object to the socket"""
    data = json.loads(data.decode("utf-8"))
    d_item = data["item"]
    d_action = data["action"]
    d_data = data["data"]
    payload = {}

    if d_item == "LOBBY":
        if d_action == "get_lobby":
            payload = LobbyInstance.get_lobby()
        elif d_action == "create_table":
            payload = LobbyInstance.create_table(d_data[0], d_data[1], d_data[2], d_data[3],
                                                 d_data[4], d_data[5], d_data[6], d_data[7])
    elif d_item == "TABLE":
        if d_action == "view_table":
            table = [table for table in LobbyInstance.tables if table.table_name == d_data[0]]
            table = table[0]
            if table.player_order:
                action_player = [player for player in table.player_order if player.action]
                action_player = action_player[0].name
                first_player = table.player_order[0].name
            else:
                action_player = None
                first_player = None
            players = {}
            for key, value in table.seats:
                if value is not None:
                    players[value.name] = [key, value.stack, value.equity, value.folded, value.active]
            if table.pots:
                pots = []
                pot_players = []
                for pot in table.pots:
                    amount = pot.amount
                    for player in pot.players:
                        pot_players.append(player.name)
                    pots.append([amount, pot_players[:]])
                    pot_players = []
            else:
                pots = []

            payload['table'] = table.table_name
            payload['table_stats'] = [len(table.seats), table.sb_amount, table.bb_amount, table.buy_in,
                                      table.ante, table.community_cards, action_player, first_player]
            payload['players'] = players
            payload['pots'] = pots

    payload = json.dumps(payload)
    return payload



