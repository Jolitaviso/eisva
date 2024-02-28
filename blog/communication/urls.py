from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('communication/', views.communication_list, name='communication_list'),
    path('communication/<int:pk>/', views.communication_detail, name='communication_detail'),
]