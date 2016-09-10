from PokerReduxe.gamelogic.table import Table


class Lobby(object):
    """  The lobby is the container object that instantiates and holds the table objects

    Attributes:
        tables(lst):  A list of all the active tables

    Methods:
        create_table:  creates a table object and adds it to the tables list

        TODO:  remove_table:   needs to remove inactive tables (tables with 0 players)"""

    def __init__(self):
        self.tables = []

    def get_lobby(self):
        payload = {"tables": []}
        for table in self.tables:
            num_players = 0
            for v in table.seats:
                if table.seats[v] is not None:
                    num_players += 1
            payload_item = {table.table_name: [num_players, len(table.seats), table.sb_amount,
                                               table.bb_amount, table.ante, table.buy_in]}
            payload["tables"].append(payload_item)
        return payload

    def create_table(self, player_name, stack, table_name, seats, sb_amount, bb_amount, buy_in, ante=0):
        if self.tables:
            for table in self.tables:
                if table_name == table.table_name:
                    raise Exception("Table Names must be unique.")
        else:
            table = Table(table_name, seats, sb_amount, bb_amount, buy_in, ante)
            table.join(1, player_name, stack)
            self.tables.append(table)
            payload = {'name': table_name, 'blinds': [sb_amount, bb_amount, ante], 'buy_in': buy_in, 'seats': seats,
                       'players': [{'name': player_name, 'stack': stack}]}
        return payload

    def get_table(self, table_name):
        table = [table for table in self.tables if table.table_name == table_name]
        return table

LobbyInstance = Lobby()
