from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from . import models

def index(request: HttpRequest) -> HttpResponse:
    context = {
        'blogs_count'.capitalize: models.Blog.objects.count(),
        'comunnications_count'.capitalize: models.Communication.objects.count(),
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