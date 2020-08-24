"""movieman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Movieman APIs",
        default_version='v1.0',
        contact=openapi.Contact(email="rj8130950@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

auth_view = swagger_auto_schema(
    method='post',
    request_body=AuthTokenSerializer
)(obtain_auth_token)


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'task', TaskViewSet)
router.register(r'movie', MovieViewSet)
router.register(r'cast', CastViewSet)
router.register(r'activity', ActivityViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', auth_view, name='login'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-docs/$', schema_view.with_ui('swagger',), name='schema-swagger-ui')
]
