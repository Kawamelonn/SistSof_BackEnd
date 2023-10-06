from django.contrib import admin
from django.urls import path, include
from SEL4C.app1 import views

urlpatterns = [
    path('', views.home, name = "homepage"),
    path('register/', views.register, name = "register"),
    path('login/', views.login_view, name = "login"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('usuarios', views.usersList, name = "users-list"),
    path('dashboard/usuario/<int:pk>', views.userDetails, name = "user-details"),
    path('dashboard/botones', views.buttons, name = "buttons"),
    path('dashboard/cards', views.cards, name = "cards"),
]