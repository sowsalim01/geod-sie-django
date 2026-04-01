from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('api/points/', views.get_points_api, name='api_points'),
]