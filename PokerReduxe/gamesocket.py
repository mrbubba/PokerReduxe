import socket
import json


from gamelogic.lobby import LobbyInstance


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
        data = json.loads(repr(data))
        d_object = data["object"]
        d_action = data["action"]
        if d_object == "Lobby":
            if d_action == "get_lobby":
                payload = LobbyInstance.get_lobby()
                payload = json.dumps(payload)
                conn.sendall(payload)
            elif d_action == "create_table"
                payload = LobbyInstance.create_table()
                payload = json.dumps(payload)
                conn.sendall(payload)
    conn.close()










