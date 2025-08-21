from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("about/", views.about, name="about"),
    path("rules/", views.rules, name="rules"),
    path("403csrf/", views.csrf_failure, name="403csrf"),
    path("404/", views.page_not_found, name="404"),
    path("500/", views.server_error_view, name="500"),
]
