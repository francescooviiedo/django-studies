from django.contrib import admin
from django.urls import path
from .views import register, create_group, login_view

urlpatterns = [
    path('register/', register),
    path('create-group/', create_group),
    path('login/', login_view),
    path('admin/', admin.site.urls),
]
