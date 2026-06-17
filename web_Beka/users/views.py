from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView as DjangoLoginView, 
    LogoutView as DjangoLogoutView
)

class LoginView(DjangoLoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')

class LogoutView(DjangoLogoutView):
    template_name = 'logout.html'
    next_page = reverse_lazy('home')