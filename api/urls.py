from django.urls import path
from . import views

# include the built-in auth urls for the built-in views

urlpatterns = [
    path('/home', views.home, name="home")
]


