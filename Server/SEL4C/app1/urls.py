from django.contrib import admin
from django.urls import path, include
from SEL4C.app1 import views
from SEL4C.app1.views import ImportarDatosCSV, SubcompetenciasAPI

urlpatterns = [
    path('', views.home, name = "homepage"),
    path('user-login/', views.user_login_view, name = "user-login"),
    path('login/', views.login_view, name = "login"),
    path('logout/', views.logout_view, name="logout"),
    path('instituciones/', views.institute_view, name="institutions"),
    path('user-login/', views.user_login_view, name = "user-login"),
    path('registrar-institucion/', views.register_institution, name="register-institution"),
    path('borrar-institucion/<int:id>', views.delete_institution, name="delete-institution"),
    path('dashboard/', views.dashboard, name = "index"),
    path('usuarios', views.usersList, name = "users-list"),
    path('dashboard/usuario/<int:pk>', views.userDetails, name = "user-details"),
    path('dashboard/botones', views.buttons, name = "buttons"),
    path('dashboard/cards', views.cards, name = "cards"),
    path('importar-datos-csv/', ImportarDatosCSV.as_view(), name='importar_datos_csv'), # esta es la url para importarle los datos solo que tiene que ser por POSTMAN
    path('api/subcompetencias/', SubcompetenciasAPI.as_view(), name='subcompetencias_api'),
]