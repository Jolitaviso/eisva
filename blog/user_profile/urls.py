from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('detail/', views.user_detail_current, name='user_detail_current'),
    path('detail/<str:username>/', views.user_detail_current, name='user_detail'),
    path('users/', views.user_list, name='user_list'),
    path('edit/', views.user_update, name='user_update'),
    path('received/', views.message_list_received, name='message_list_received'),  
    path('sent/', views.message_list_sent, name='message_list_sent'),  
    path('create/', views.MessageCreateView.as_view(), name='message_create'),
    path('user/<str:username>/blogs/', views.user_blogs, name='user_blogs'),
    
]
