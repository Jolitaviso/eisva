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
from . import models, forms
from django.db.models import Count
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
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: 
        context = super().get_context_data(**kwargs)
        return context
    
class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Blog
    template_name = 'communication/blog_create.html'
    fields = ('name', 'description', 'youtube_video' )
    autocomplete_fields = ['owner']
    
    def get_success_url(self) -> str:
        messages.success(self.request,
            _('blog created successfully').capitalize())
        return reverse('blog_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    
    
    '''def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.owner = self.request.user
        return form

    def get_success_url(self) -> str:
        messages.success(self.request, _('blog created successfully').capitalize())
        return reverse('blog_list')'''
    

class BlogUpdateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.UpdateView
    ):
    model = models.Blog
    template_name = 'communication/blog_update.html'
    fields = ('name', 'owner', 'description', 'youtube_video')

    def get_success_url(self) -> str:
        messages.success(self.request, _('blog updated successfully').capitalize())
        return reverse('blog_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
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
    communications = models.Communication.objects.all()
    popular_blogs = models.Blog.objects.annotate(num_communications=Count('communications')).order_by('-num_communications')[:5]
    common_home = [
        (_('users').title(), get_user_model().objects.count()),
        (
            _('blogs').title(), 
            models.Blog.objects.count(), 
            reverse('blog_list'),
        ),
        (
            _('communications').title(), 
            communications.count(), 
            reverse('communication_list'),
        ),
    ]
    if request.user.is_authenticated:
        user_communications = communications.filter(owner=request.user)
        user_home = [
            (
                _('blogs').title(), 
                models.Blog.objects.filter(owner=request.user).count(), 
                reverse('blog_list') + f"?owner={request.user.username}",
            ),
            (
                _('communications').title(), 
                user_communications.count(),
                reverse('communication_list') + f"?owner={request.user.username}",
            ),
        ]
    else:
        user_home = None
    context = {
        'common_home': common_home,
        'user_home': user_home,
        'popular_blogs': popular_blogs,
        
    }
    return render(request, 'communication/index.html', context)


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
        blog = get_object_or_404(models.Blog, pk=blog_pk)
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


def communication_detail(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'communication/communication_detail.html', {
        'communication': get_object_or_404(models.Communication, pk=pk),
    })
    
    
@login_required
def communication_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.CommunicationForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request, _("communication created successfully").capitalize())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('communication_list')
    else:
        form = forms.CommunicationForm()
    form.fields['blog'].queryset = models.Blog.objects.all()
    #form.fields['blog'].queryset = form.fields['blog'].queryset.filter(owner=request.user)
    return render(request, 'communication/communication_create.html', {'form': form})

@login_required
def communication_update(request: HttpRequest, pk: int) -> HttpResponse:
    communication = get_object_or_404(models.Communication, pk=pk, owner=request.user)
    if request.method == "POST":
        form = forms.CommunicationForm(request.POST, instance=communication)
        if form.is_valid():
            form.save()
            messages.success(request, _("communication edited successfully").capitalize())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('communication_list')
    else:
        form = forms.CommunicationForm(instance=communication)
    form.fields['blog'].queryset = models.Blog.objects.all()
    #form.fields['blog'].queryset = form.fields['blog'].queryset.filter(owner=request.user)
    return render(request, 'communication/communication_update.html', {'form': form})

@login_required
def communication_delete(request: HttpRequest, pk: int) -> HttpResponse:
    communication = get_object_or_404(models.Communication, pk=pk, owner=request.user)
    if request.method == "POST":
        communication.delete()
        messages.success(request, _("communication deleted successfully").capitalize())
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('communication_list')
    return render(request, "communication/communication_delete.html", {'communication': communication, 'object': communication})


@login_required
def blog_like(request: HttpRequest, pk: int) -> HttpResponse:
    blog = get_object_or_404(models.Blog, pk=pk)
    like = models.BlogLike.objects.filter(blog=blog, user=request.user).first()
    if not like:
        models.BlogLike.objects.create(blog=blog, user=request.user)
    else:
        like.delete()
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('blog_list')

@login_required
def communication_like(request: HttpRequest, pk: int) -> HttpResponse:
    communication = get_object_or_404(models.Communication, pk=pk)
    like = models.CommunicationLike.objects.filter(communication=communication, user=request.user).first()
    if not like:
        models.CommunicationLike.objects.create(communication=communication, user=request.user)
    else:
        like.delete()
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('communication_list')

@login_required
def comment_create(request):
    if request.method == 'POST':
        communication_pk = request.POST.get('communication_pk')
        note = request.POST.get('note')
        owner = request.user 
        communication = get_object_or_404(models.Communication, pk=communication_pk)
        models.Comment.objects.create(communication=communication, owner=owner, note=note)
        return redirect('communication_detail', pk=communication_pk)
    
def comment_detail(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'communication/comment_detail.html', {
        'comment': get_object_or_404(models.Comment, pk=pk),
    })