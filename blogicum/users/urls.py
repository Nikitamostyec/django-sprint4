from django.urls import path
from .views import LoginUser

urlpatterns = [
    path('registration/', LoginUser.as_view(), name='registration')
]
