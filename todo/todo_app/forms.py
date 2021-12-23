from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TodoUserForm(UserCreationForm):
    telegram_id = forms.IntegerField(required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.telegram_id = self.cleaned_data["telegram_id"]
        if commit:
            user.save()
        else:
            return user

    class Meta:
        model = User
        fields = ("username", "telegram_id", "password1", "password2")
