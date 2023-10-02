"""
URL configuration for SEL4C project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from rest_framework import routers, permissions
from SEL4C.app1 import views
from drf_spectacular.views import SpectacularAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'Administradores', views.AdministradorViewSet)
router.register(r'Usuarios', views.UsuarioViewSet)
router.register(r'Progresos', views.ProgresoViewSet)
router.register(r'Actividades', views.ActividadViewSet)
router.register(r'Entregas', views.EntregaViewSet)
router.register(r'Autodiagnosticos', views.AutodiagnosticoViewSet)
router.register(r'Preguntas', views.PreguntaViewSet)
router.register(r'Respuesta', views.RespuestaViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snipets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/schema/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('SEL4C/', views.home, name = "homepage"),
    path('SEL4C/register/', views.register, name = "register"),
    path('SEL4C/login/', views.login, name = "login"),
    path('SEL4C/dashboard/', views.dashboard, name = "index"),
    path('SEL4C/dashboard/usuarios', views.usersList, name = "users-list"),
    path('SEL4C/dashboard/usuario/<int:pk>', views.userDetails, name = "user-details"),
    path('SEL4C/dashboard/botones', views.buttons, name = "buttons"),
    path('SEL4C/dashboard/cards', views.cards, name = "cards"),
]