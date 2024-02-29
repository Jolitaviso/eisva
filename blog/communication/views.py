from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from . import models

class BlogListView(generic.ListView):
    model = models.Blog
    template_name = 'communication/blog_list.html'


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
        return self.get_object().owner == self.request.user
    
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
        return self.get_object().owner == self.request.user
    
    
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