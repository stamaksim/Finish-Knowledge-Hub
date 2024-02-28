from django import forms
from django.forms import ModelForm

from knowhub.models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text", )
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control mb-3",
                "rows": 3
            }),
        }