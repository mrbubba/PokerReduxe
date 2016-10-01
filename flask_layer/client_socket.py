import socket


def client_socket(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    sock.connect(server_address)
    sock.sendall(data)
    payload = sock.recv(1024)
    payload = json.loads(payload)
    return payload