from django.shortcuts import render
from django.views.generic.base import TemplateView


class LobbyView(TemplateView):

    allowed_methods = ['get']
    template_name = 'lobby/lobby.html'

    def get(self, request, *args, **kwargs):
        """Serves up the lobby template"""

        context = {'title': 'Bibble'}

        return render(request, self.template_name, context)