from django.urls import path
from remindapp import admin_views as views

urlpatterns = [
    path('home', views.home , name="admin_home"),
    path('levels', views.level, name='levels'),
    path('add_level', views.addLevel, name='add_level'),
    path('edit_level/<str:pk>', views.editLevel, name='edit_level'),
    path('delete_level/<str:pk>', views.deleteLevel, name='delete_level'),
    path('courses', views.courses, name='courses'),
    path('add_course', views.addCourse, name='add_course'),
]