from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/create/', views.BlogCreateView.as_view(), name='blog_create'),  
    path('blog/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),  
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('communications/', views.communication_list, name='communication_list'),
    path('communication/<int:pk>/', views.communication_detail, name='communication_detail'),
    path('communication/create/', views.communication_create, name='communication_create'),
    path('communication/<int:pk>/edit/', views.communication_update, name='communication_update'),
    path('communication/<int:pk>/delete/', views.communication_delete, name='communication_delete'),
    path('blog/<int:pk>/like/', views.blog_like, name='blog_like'),
    path('communication/create/<int:blog_id>/', views.communication_create, name='communication_create'),
    path('communication/<int:pk>/like/', views.communication_like, name='communication_like'),   
    path('comment/create/', views.comment_create, name='comment_create'), 
    path('communication/<int:pk>/comment/<int:comment_pk>/', views.comment_detail, name='comment_detail'),

]