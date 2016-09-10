import socket
from poker_api.handler import handler

from PokerReduxe.gamelogic.lobby import Lobby
LobbyInstance = Lobby()


def socket_server():
    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    s.bind(server_address)
    s.listen(5)
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        payload = handler(data)
        conn.sendall(payload)
    conn.close()
