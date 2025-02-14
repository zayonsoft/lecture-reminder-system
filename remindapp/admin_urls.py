from django.urls import path
from remindapp import admin_views as views

urlpatterns = [
    path('home', views.home , name="admin_home"),
    path('levels', views.level, name='levels'),
    path('add_level', views.addLevel, name='add_level'),
]