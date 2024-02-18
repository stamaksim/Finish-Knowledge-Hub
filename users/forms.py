from django import forms
from django.contrib.auth.forms import UserCreationForm
from knowhub.models import User

class CustomerUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]
