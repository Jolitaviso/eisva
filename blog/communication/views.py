from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from . import models
from datetime import datetime
from typing import Any

class BlogListView(generic.ListView):
    model = models.Blog
    template_name = 'communication/blog_list.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('owner'):
            queryset = queryset.filter(owner__username=self.request.GET.get('owner'))
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_list'] = get_user_model().objects.all().order_by('username')
        return context


class BlogDetailView(generic.DetailView):
    model = models.Blog
    template_name = 'communication/blog_detail.html'
    
    
class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Blog
    template_name = 'communication/blog_create.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, _('blog created successfully').capitalize())
        return reverse('blog_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class BlogUpdateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.UpdateView
    ):
    model = models.Blog
    template_name = 'communication/blog_update.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, _('blog updated successfully').capitalize())
        return reverse('blog_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user or self.request.user.is_superuser
    
class BlogDeleteView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.DeleteView
    ):
    model = models.Blog
    template_name = 'communication/blog_delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, _('blog deleted successfully').capitalize())
        return reverse('blog_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user or self.request.user.is_superuser
    
    
def index(request: HttpRequest) -> HttpResponse:
    context = {
        'blogs_count'.capitalize: models.Blog.objects.count(),
        'communnications_count'.capitalize: models.Communication.objects.count(),
        'users_count'.capitalize: models.get_user_model().objects.count(),
        'comments_count'.capitalize: models.Comment.objects.count(),
    }
    return render(request, 'communication/index.html/', context)

def communication_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'communication/communication_list.html', {
        'communication_list': models.Communication.objects.all(),
    })
    
def communication_detail(request: HttpRequest, pk:int) -> HttpResponse:
    return render(request, 'communication/communication_detail.html', {
        'communication': get_object_or_404(models.Communication, pk=pk)
    })
    
def communication_list(request: HttpRequest) -> HttpResponse:
    queryset = models.Communication.objects
    owner_username = request.GET.get('owner')
    if owner_username:
        owner = get_object_or_404(get_user_model(), username=owner_username)
        queryset = queryset.filter(owner=owner)
        '''blogs = models.Blog.objects.filter(owner=owner)
    elif request.user.is_authenticated:
        blogs = models.Blog.objects.filter(owner=request.user)
    else:
        blogs = models.Blog.objects'''
    blog_pk = request.GET.get('blog_pk')
    if blog_pk:
        blog = get_object_or_404(models.blog, pk=blog_pk)
        queryset = queryset.filter(blog=blog)
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    context = {
        'communication_list': queryset.all(),
        'blog_list': models.Blog.objects.all(),
        'user_list': get_user_model().objects.all().order_by('username'),
    }
    return render(request, 'communication/communication_list.html', context)