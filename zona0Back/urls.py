"""
URL configuration for zona0Back project.

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
from django.urls import path, re_path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi 
from rest_framework import permissions

from apps.users.api.views.manager_view import ManagerCreateView


schema_view = get_schema_view(
    openapi.Info(
        title = "Zona0 API",
        default_version = "version 1.0",
        description = "Public Documentation of Zona0 Rest Api",
        terms_of_service = "https://www.google.com/policies/terms/",
        contact = openapi.Contact(email ="mangelryujin@gmail.com"),
        License = openapi.License(name = "BSD License"),     
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/', include('apps.users.api.routers')),
    path('users/', include('apps.users.api.routers2')),
    path('institutions/', include('apps.institution.api.routers')),
    path('redeem-code/', include('apps.redeem.api.routers')),
    # path('transfers/orders/', include('apps.orders.api.routers')),
    re_path(r'^swagger(?P<format>\.json/\.yaml)$', schema_view.without_ui(cache_timeout=0), name = 'schema-json'),
    path('api-docs/', schema_view.with_ui('swagger',cache_timeout=0), name = 'schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name = 'schema-swagger-redoc'),
    path("accounts/", include("apps.users.urls")),
    path("manager/register/", ManagerCreateView.as_view(), name="manager_register"),
    path("manager/", include('apps.manager.urls')),
    path("transfer/", include('apps.orders.urls')),
]
