from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class CommunicationForm(forms.ModelForm):
    class Meta:
        model = models.Communication
        fields = ('name', 'blog', 'description' )
        widgets = {
            'updated_at': DateInput,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['id', 'title', 'note', 'image','communication', 'parent_comment']
        