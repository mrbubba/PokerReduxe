from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.


def register(request):

    template = 'accounts/register.html'
    register_form = RegisterForm(request.POST or None)

    context = {'register_form': register_form}

    if register_form.is_valid():

        register_form.save()

        context = {'Thanks': "Thanks for the memories"}


    return render(request, template, context)
