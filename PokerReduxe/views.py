from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from PokerReduxe.gamelogic.lobby import Lobby


class LobbyView(TemplateView):
    allowed_methods = ["post", "get"]

    def get(self, request, *args, **kargs):
        """proccess and deliver information to lobby"""




        return render(request,)
