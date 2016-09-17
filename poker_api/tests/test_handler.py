import json
import unittest

from PokerReduxe.gamelogic.card import Card
from PokerReduxe.gamelogic.lobby import LobbyInstance
from PokerReduxe.gamelogic.pot import Pot
from poker_api.handler import handler, handler_response


class TestHandler(unittest.TestCase):
    def setUp(self):
        self.lobby = LobbyInstance

        self.lobby.create_table("Bubba", 100, "testable", 6, 2, 4, [50, 100], 0)
        bc1 = Card("10_hearts", 10, "h")
        bc2 = Card("Ace_hearts", 14, "h")
        self.lobby.tables[-1].seats[1].hole_cards = [bc1, bc2]
        self.lobby.tables[-1].seats[1].action = True
        self.lobby.tables[-1].seats[1].equity = 2
        self.lobby.tables[-1].join(2, "Martha", 100)
        mc1 = Card("7_diamonds", 7, "d")
        mc2 = Card("2_clubs", 2, "c")
        self.lobby.tables[-1].seats[2].hole_cards = [mc1, mc2]
        self.lobby.tables[-1].seats[2].equity = 10
        cc1 = Card("King_hearts", 13, "h")
        cc2 = Card("9_hearts", 9, "h")
        cc3 = Card("Jack_hearts", 11, "h")
        self.lobby.tables[-1].player_order.append(self.lobby.tables[-1].seats[1])
        self.lobby.tables[-1].player_order.append(self.lobby.tables[-1].seats[2])
        self.lobby.tables[-1].community_cards.append(cc1)
        self.lobby.tables[-1].community_cards.append(cc2)
        self.lobby.tables[-1].community_cards.append(cc3)
        pot1 = Pot(self.lobby.tables[-1].player_order, 100)
        pot2 = Pot(self.lobby.tables[-1].player_order, 100)
        self.lobby.tables[-1].pots = [pot1, pot2]

        self.lobby.create_table("Bubba", 100, "testable2", 6, 2, 4, [50, 100], 0)
        self.lobby.tables[-1].seats[1].hole_cards = [bc1, bc2]
        self.lobby.tables[-1].seats[1].action = True
        self.lobby.tables[-1].seats[1].equity = 2
        self.lobby.tables[-1].join(2, "Martha", 100)
        self.lobby.tables[-1].seats[2].hole_cards = [mc1, mc2]
        self.lobby.tables[-1].seats[2].equity = 10
        self.lobby.tables[-1].player_order.append(self.lobby.tables[-1].seats[1])
        self.lobby.tables[-1].player_order.append(self.lobby.tables[-1].seats[2])
        self.lobby.tables[-1].community_cards.append(cc1)
        self.lobby.tables[-1].community_cards.append(cc2)
        self.lobby.tables[-1].community_cards.append(cc3)
        self.lobby.tables[-1].pots = [pot1, pot2]

    def test_get_lobby(self):
        """  can we get the table list from lobby?"""
        data = {"item": "LOBBY", "action": "get_lobby", "data": []}
        data = json.dumps(data)
        data = data.encode()
        result = handler(data)
        expected = {"tables": {"testable": [2, 6, 2, 4, 0, [50, 100]],
                               "testable2": [2, 6, 2, 4, 0, [50, 100]]}}
        self.assertEqual(expected, result)

    def test_response(self):
        """can we get all of the data for a table object?"""
        result = handler_response(self.lobby.tables[0])

        expected = {"table": "testable", "table_stats":
            [6, 2, 4, [50, 100], 0, ["King_hearts", "9_hearts", "Jack_hearts"],
             "Bubba", "Bubba"], "players": {"Bubba": [1, 100, 2, False, True, "10_hearts", "Ace_hearts"],
                                            "Martha": [2, 100, 10, False, True, "7_diamonds", "2_clubs"]},
                    "pots": [[100, ["Bubba", "Martha"]], [100, ["Bubba", "Martha"]]]}
        self.assertEqual(expected, result)

    def tearDown(self):
        self.lobby.tables = []


if __name__ == '__main__':
    unittest.main()
