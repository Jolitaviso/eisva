from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views import generic
from . import models
from . import forms
from django.shortcuts import render
from communication.models import Blog


User = get_user_model()

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Thank you! You can log in now with your credentials."))
            return redirect("index")
    else:
        form = forms.CreateUserForm()
    return render(request, 'user_profile/signup.html', {
        'form': form,
    })

@login_required
def user_detail_current(request: HttpRequest, username: str | None = None)  -> HttpResponse:
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    return render(request, 'user_profile/user_detail_current.html', {
        'object': user,
    })
    
@login_required
def user_update(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form_user = forms.UserForm(request.POST, instance=request.user)
        form_profile = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            messages.success(request, _("Profile edited successfully").capitalize())
            return redirect('user_detail_current')
    else:
        form_user = forms.UserForm(instance=request.user)
        form_profile = forms.ProfileForm(instance=request.user.profile)
    return render(request, 'user_profile/user_update.html', {
        'form_user': form_user,
        'form_profile': form_profile,
    }) 

@login_required
def user_list(request):
    users = get_user_model().objects.all().order_by('username')
    return render(request, 'user_profile/user_list.html', {'users': users})

class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Message
    template_name = 'user_profile/message_create.html'
    form_class = forms.MessageForm

    def get_success_url(self) -> str:
        messages.success(self.request, _('message created successfully').capitalize())
        return reverse('message_list_sent')
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.save()
        return super().form_valid(form)
  

@login_required
def message_list_sent(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_messages = models.Message.objects.filter(sender=user)

    receiver_username = request.GET.get('receiver')
    if receiver_username:
        receiver = get_object_or_404(get_user_model(), username=receiver_username)
        user_messages = user_messages.filter(receiver=receiver)

    context = {
        'message_list_sent': user_messages,
        'user_list': get_user_model().objects.all().order_by('username'),
        'next': reverse('message_list_sent') + '?' + \
            '&'.join([f"{key}={value}" for key, value in request.GET.items()]),
        'no_matches': not user_messages.exists(),
    }
    return render(request, 'user_profile/message_list_sent.html', context)

@login_required
def message_list_received(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_messages = models.Message.objects.filter(receiver=user)

    sender_username = request.GET.get('sender')
    if sender_username:
        sender = get_object_or_404(get_user_model(), username=sender_username)
        user_messages = user_messages.filter(sender=sender)

    context = {
        'message_list_received': user_messages,
        'user_list': get_user_model().objects.all().order_by('username'),
        'next': reverse('message_list_received') + '?' + \
            '&'.join([f"{key}={value}" for key, value in request.GET.items()]),
        'no_matches': not user_messages.exists(),
    }
    return render(request, 'user_profile/message_list_received.html', context)

def user_blogs(request, username):
    user = get_user_model().objects.get(username=username)
    user_blogs = Blog.objects.filter(owner=user)
    return render(request, 'user_profile/user_blogs.html', {'user_blogs': user_blogs})