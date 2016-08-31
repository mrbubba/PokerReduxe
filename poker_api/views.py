from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import socket


def game_socket(payload):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    sock.connect(server_address)
    sock.sendall(payload)
    data = sock.recv(1024)
    sock.close()
    return data


class LobbyView(APIView):

    def get(self, request):
        data = game_socket("GETLOBBY")
        #  TODO:  convert data in Json and return it to the client via websocket
        return Response(data)
