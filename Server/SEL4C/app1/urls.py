from django.contrib import admin
from django.urls import path, include
from SEL4C.app1 import views

urlpatterns = [
    path('', views.home, name = "homepage"),
    path('register/', views.register, name = "register"),
    path('login/', views.login_view, name = "login"),
    path('logout/', views.logout_view, name="logout"),
    path('instituciones/', views.institute_view, name="institutions"),
    path('registrar-institucion/', views.register_institution, name="register-institution"),
    path('dashboard/', views.dashboard, name = "index"),
    path('usuarios', views.usersList, name = "users-list"),
    path('dashboard/usuario/<int:pk>', views.userDetails, name = "user-details"),
    path('dashboard/botones', views.buttons, name = "buttons"),
    path('dashboard/cards', views.cards, name = "cards"),
]