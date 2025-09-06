from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def csrf_failure(request, reason=''):
    return render(request,
                  'pages/403csrf.html',
                  {'reason': reason},
                  status=403)


def page_not_found(request, exception=None):
    return render(request, 'pages/404.html', status=404)


def server_error_view(request):
    return render(request, 'pages/500.html', status=500)


def about(request):
    return render(request, "pages/about.html")


def rules(request):
    return render(request, "pages/rules.html")


class RegistationView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("login")
