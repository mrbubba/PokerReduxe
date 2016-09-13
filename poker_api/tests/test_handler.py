import unittest
import json


from poker_api.handler import handler
from PokerReduxe.gamelogic.lobby import Lobby, LobbyInstance
from PokerReduxe.gamelogic.table import Table


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.lobby = LobbyInstance
        self.lobby.create_table("Bubba", 100, "testable", 6, 2, 4, [50, 100], 0)

    def test_get_lobby(self):
        """  can we get the table list from lobby?"""
        data = {"item": "LOBBY", "action": "get_lobby", "data": []}
        data = json.dumps(data)
        data = data.encode()
        payload = handler(data)
        result = {"tables":  [{"testable": [1, 6, 2, 4, 0, [50, 100]]}]}
        result = json.dumps(result)
        self.assertEqual(result, payload)

    def test_create_table(self):
        """  Can we create a table ??"""
        data = {"item": "LOBBY", "action": "create_table", "data":
                ["Bubba", 100, "testable2", 6, 2, 4, [50, 100], 0]}
        data = json.dumps(data)
        data = data.encode()
        handler(data)
        self.assertEqual(LobbyInstance.tables[-1].table_name, "testable2")

    def test_table_with_the_same_name_exception(self):
        """  Do we get an exception if the table name is not unique"""
        data = {"item": "LOBBY", "action": "create_table", "data":
            ["Bubba", 100, "testable", 6, 2, 4, [50, 100], 0]}
        data = json.dumps(data)
        data = data.encode()
        with self.assertRaises(Exception):
            handler(data)
        self.assertEqual(1, len(self.lobby.tables))

    def test_view_table(self):
        """  Can we get all of the information we need from a table??"""
        data = {"item": "TABLE", "action": "view_table", "data": ['testable']}
        result = {'table': 'testable', 'table_stats': [6, 2, 4, [50, 100], 0, [], None, None],
                  'players': {'Bubba': [1, 100, 0, False, True]}, 'pots': []}

    def tearDown(self):
        self.lobby.tables = []


if __name__ == '__main__':
    unittest.main()
