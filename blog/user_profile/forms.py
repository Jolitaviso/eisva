from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models
from django.utils.translation import gettext_lazy as _

class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''


class UserForm(forms.ModelForm):
    description = forms.CharField(label=_("description"), widget=forms.Textarea)
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", 'description' )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ("picture", )

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = self.fields['receiver'].queryset.order_by('username')

    class Meta:
        model = models.Message
        fields = ('text', 'document', 'image', 'receiver')