from django.urls import path

from . import views
from .views import RulesPageView, AboutPageView

app_name = "pages"

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),
    path("rules/", RulesPageView.as_view(), name="rules"),
]
