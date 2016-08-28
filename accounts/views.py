from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

from .forms import RegisterForm, LoginForm
# Create your views here.


class RegisterView(TemplateView):
    allowed_methods = ["post", "get"]
    template_name = 'accounts/register.html'
    register_form = RegisterForm()

    def post(self, request, *args, **kargs):
        form = RegisterForm(request.POST)
        is_valid = form.is_valid()

        if is_valid is False:
            return render(request, self.template_name, {'register_form': form})
        else:
            name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=name, password=password)
            user.save()

            return redirect('/accounts/login')
            # redirect logic

    def get(self, request, *args, **kargs):
        return render(request, self.template_name, { 'register_form': self.register_form })


class LoginView(TemplateView):
    allowed_methods = ["post", "get"]
    template_name = 'accounts/login.html'

    def post(self, request, *args, **kargs):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, { "login_form": form })

        user = authenticate(username=form.cleaned_data["user_name"], password=form.cleaned_data["password"])

        if user is None:
            # TODO: Add custom error message to form as non_field_error
            return render(request, self.template_name, { "login_form": form })
        login(request, user)
        return redirect("/lobby")

    def get(self, request, *args, **kargs):
        form = LoginForm()
        return render(request, self.template_name, { "login_form": form } )
