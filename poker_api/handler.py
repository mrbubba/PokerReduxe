import json

from PokerReduxe.gamelogic.lobby import LobbyInstance


def handler(data):
    """takes the data json object from the socket, makes the python calls to the game server,
    and returns the payload json object to the socket"""
    data = json.loads(data.decode("utf-8"))
    d_item = data["item"]
    d_action = data["action"]
    d_data = data["data"]

    if d_item == "LOBBY":
        if d_action == "get_lobby":
            payload = LobbyInstance.get_lobby()

    payload = json.dumps(payload)
    return payload
