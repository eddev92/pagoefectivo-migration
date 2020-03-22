from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('notification/', views.indexNotification, name="notification"),
    path('configuration/', views.indexConfiguration, name="configuration"),
    url(r'^validation/', views.IdealWeight)
]