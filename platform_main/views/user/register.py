from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django import forms
from django.http import HttpRequest
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist

from platform_main.models import User


class RegisterForm(forms.Form):
    email = forms.CharField(max_length=100, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=100)
    name = forms.CharField(max_length=100, min_length=3)


class RegisterView(View):
    template_name = 'registration/login.html'

    def get(self, request: HttpRequest):
        form = RegisterForm()
        return render(request, 'v2/auth/register.html', {'form': form})

    def post(self, request: HttpRequest):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.data['email'])
            except ObjectDoesNotExist:
                pass
            else:
                return render(request, 'v2/auth/register.html', {'form': form, 'message': 'User already exists!'})
        else:
            print(form.errors.as_data())
            return render(request, 'v2/auth/register.html', {'form': form})
        user = User.create_user(form.data['email'],
                                form.data['password'],
                                form.data['name'])
        login(request, user)
        return HttpResponseRedirect(redirect_to="/home")
