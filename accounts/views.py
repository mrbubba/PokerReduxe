from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic.base import TemplateView

from .forms import RegisterForm
# Create your views here.


class RegisterView(TemplateView):
    allowed_methods = ["post", "get"]
    template_name = 'accounts/register.html'
    register_form = RegisterForm()
    def post(self, request, *args, **kargs):
        form = RegisterForm(request.POST)
        is_valid = form.is_valid()

        if is_valid is False:
            return render(request, self.template_name, { 'register_form': form })
        else:
            # redirect logic
            pass


    def get(self, request, *args, **kargs):
        return render(request, self.template_name, { 'register_form': self.register_form })


def register(request):

    template = 'accounts/register.html'
    register_form = RegisterForm(request.POST or None)

    context = {'register_form': register_form}

    if register_form.is_valid():
        user_name = register_form.cleaned_data.get('user_name')
        password = register_form.cleaned_data.get('password')
        user = User.objects.create_user(user_name, password)
        user.save()

        context = {'Thanks': "Thanks for the memories"}


    return render(request, template, context)


def login(request):

    template = 'accounts/login.html'
    login_form = LoginForm(request.POST)
