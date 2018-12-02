from django.urls import path

from . import views

app_name = 'assignment2'
urlpatterns = [
    path('', views.index, name='index'),
    path('k_means/', views.k_means, name='k_means'),
    path('hierarchical/', views.hierarchical, name='hierarchical'),
    path('load/', views.load_data, name='load'),
]
