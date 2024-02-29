from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('communication/', views.communication_list, name='communication_list'),
    path('communication/<int:pk>/', views.communication_detail, name='communication_detail'),
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/create/', views.BlogCreateView.as_view(), name='blog_create'),  
    path('blog/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),  
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
]