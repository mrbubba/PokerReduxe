import unittest
import json


from poker_api.handler import handler
from PokerReduxe.gamelogic.lobby import Lobby, LobbyInstance
from PokerReduxe.gamelogic.table import Table


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.lobby = LobbyInstance
        self.lobby.create_table("Bubba", 100, "testable", 6, 2, 4, [50, 100])

    def test_get_lobby(self):
        """  can we get the table list from lobby?"""
        data = {"item": "LOBBY", "action": "get_lobby", "data": []}
        data = json.dumps(data)
        data = data.encode()
        payload = handler(data)
        result = {"tables":  [{"testable": [1, 6, 2, 4, 0, [50, 100]]}]}
        result = json.dumps(result)
        self.assertEqual(result, payload)

if __name__ == '__main__':
    unittest.main()
