from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('explorer/', views.explorer, name="explorer"),
    path('signup', views.signup, name='signup'),
    path('login', views.loginhandel, name='login'),
    path('search', views.search, name='search'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('about', views.about, name='about'),
]
