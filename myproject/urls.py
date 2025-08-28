from django.contrib import admin
from django.urls import path
from .views import register, create_group, login_view, testelogin, testelogin_screen, api_login, api_csrf_token

urlpatterns = [
    path('register/', register),
    path('create-group/', create_group),
    path('login/', login_view),
    path('testelogin/', testelogin, name='testelogin'),  # endpoint API
    path('testelogin-screen/', testelogin_screen, name='testelogin_screen'),  # tela HTML
    path('admin/', admin.site.urls),
    path('testelogin/', testelogin),
    path('api/login/', api_login, name='api_login'),
    path('api/csrf-token/', api_csrf_token, name='api_csrf_token'),
]
