from django.urls import path

from . import views

app_name = 'assignment1'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('recommendation', views.recommendation, name='recommendation'),
    path('load', views.load_data, name='load'),
]
