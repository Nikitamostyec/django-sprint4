from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class LoginUser(CreateView):
    form_class = UserCreationForm
    templates_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')