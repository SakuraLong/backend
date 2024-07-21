from django.urls import path

from .views import login

urlpatterns = [
    path("user/login", login)
]

whitelist = [
    "/user/login"
]