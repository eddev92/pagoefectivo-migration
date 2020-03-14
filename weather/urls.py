from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('notification/', views.indexNotification, name="notification"),
    path('configuration/', views.indexConfiguration, name="configuration"),
]