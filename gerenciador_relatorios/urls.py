"""
URL configuration for gerenciador_relatorios project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.urls import path, include
from django.contrib import admin
from drf_yasg import openapi

from api.views import redirect_if_not_authenticated, redirect_logout



schema_view = get_schema_view(
    openapi.Info(
        title="Gerenciador de Relatorios",
        default_version='1.0.0',
        description="API documentation of App"
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('api.urls')),  # Inclui as URLs da sua aplicação principal (app 'api')
    path('swagger/schema/', redirect_if_not_authenticated(schema_view.with_ui('swagger', cache_timeout=0)), name='swagger-schema'),
    path('accounts/logout/', redirect_logout(schema_view.with_ui('swagger', cache_timeout=0)))
]
