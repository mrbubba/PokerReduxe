import socket
import json


def client_socket(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    sock.connect(server_address)
    data = json.dumps(data)
    data = data.encode()
    sock.sendall(data)


    payload = sock.recv(1024)
    payload = payload.decode('utf-8')
    payload = json.loads(payload)
    return payload
