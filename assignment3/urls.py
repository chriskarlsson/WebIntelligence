from django.urls import path

from . import views

app_name = 'assignment3'
urlpatterns = [
    path('', views.index, name='index'),
]
