from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('detail/', views.user_detail_current, name='user_detail_current'),
    path('detail/<str:username>/', views.user_detail_current, name='user_detail'),
    path('list/<str:username>/', views.user_list, name='user_list'),
    path('edit/', views.user_update, name='user_update'),
]
