import socket


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
        data = repr(data)
        if "GETLOBBY" in data:
            payload = LobbyInstance.get_lobby()
            conn.sendall(payload)
    conn.close()
