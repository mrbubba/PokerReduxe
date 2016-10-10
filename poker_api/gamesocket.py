import socket
from poker_api.handler import handler


from gameserver.gamelogic.lobby import Lobby
LobbyInstance = Lobby()


def socket_server():
    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    s.bind(server_address)
    s.listen(5)
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        if not data:
            break
        payload = handler(data)
        payload = payload.encode()
        conn.sendall(payload)
    conn.close()


socket_server()
