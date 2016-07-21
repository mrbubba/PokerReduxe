from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
# Create your views here.


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
