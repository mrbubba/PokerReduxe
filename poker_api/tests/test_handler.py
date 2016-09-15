import unittest
import json


from poker_api.handler import handler
from PokerReduxe.gamelogic.lobby import Lobby, LobbyInstance
from PokerReduxe.gamelogic.card import Card


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.lobby = LobbyInstance
        self.lobby.create_table("Bubba", 100, "testable", 6, 2, 4, [50, 100], 0)
        self.lobby.tables[0].player_order.append(self.lobby.tables[0].seats[1])
        self.lobby.tables[0].player_order[0].action = True

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
        expected = {'table': 'testable', 'table_stats': [6, 2, 4, [50, 100], 0, [], 'Bubba', 'Bubba'],
                    'players': {'Bubba': [1, 100, 0, False, True]}, 'pots': []}
        data = json.dumps(data)
        data = data.encode()
        result = handler(data)
        result = json.loads(result)
        self.assertEqual(result, expected)

    def test_get_hole_cards(self):
        """can we get the names of our hole cards??"""
        c1 = Card("10c", 10, "c")
        c2 = Card("10d", 10, "d")
        self.lobby.tables[0].seats[1].hole_cards.append(c1)
        self.lobby.tables[0].seats[1].hole_cards.append(c2)
        data = {"item": "TABLE", "action": "get_hole_cards", "data": ["testable", "Bubba"]}
        expected = {'hole_cards': ["10c", "10d"]}
        data = json.dumps(data)
        data = data.encode()
        result = handler(data)
        result = json.loads(result)
        self.assertEqual(expected, result)

    def test_change_seat(self):
        """can we change to a new seat"""
        data = {'item': 'TABLE', 'action': 'change_seat', 'data': ['testable', 'Bubba', 2]}
        expected = {"player_name": "Bubba", "seat_key": 2}
        data = json.dumps(data)
        data = data.encode()
        result = handler(data)
        result = json.loads(result)
        self.assertEqual(expected, result)

    def test_join(self):
        """can we join a table??"""
        data = {'item': 'TABLE', 'action': 'join_table', 'data': ['testable', 'Martha', 2, 100]}
        expected = {'player_name': 'Martha', 'player_stack': 100, 'seat': 2}
        data = json.dumps(data)
        data = data.encode()
        result = handler(data)
        result = json.loads(result)
        self.assertEqual(expected, result)
        self.assertTrue(self.lobby.tables[0].seats[2].name == 'Martha')

    def test_quit(self):
        """Can we quit a game?"""
        data = {'item': 'TABLE', 'action': 'quit', 'data': ['testable', 'Bubba']}
        expected = {"QUIT": "Bubba"}
        data = json.dumps(data)
        data = data.encode()
        result = handler(data)
        result = json.loads(result)
        self.assertEqual(expected, result)
        self.assertFalse(self.lobby.tables[0].seats[1])

    def tearDown(self):
        self.lobby.tables = []


if __name__ == '__main__':
    unittest.main()
