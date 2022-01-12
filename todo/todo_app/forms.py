from django import forms
from django.forms import ModelForm
from .models import Tag, TodoItem, Account

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title']


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['group', 'telegram_id']
        # TODO Create Group Droplist (Andrew)
        group = forms.CharField(max_length=50)
        telegram_id = forms.IntegerField()

    def clean_telegram_id(self):
        telegram = self.cleaned_data.get('telegram_id')
        if len(str(telegram)) != 10:
            raise forms.ValidationError('You must enter a valid telegram id', code='invalid')


class CustomChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return user.username


class TodoItemForm(ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'content', 'assignee', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'tag_widget'}),
            'title': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea
        }
        field_classes = {'assignee': CustomChoiceField}
        title = forms.CharField()
        content = forms.CharField()
        assignee = CustomChoiceField(queryset=User.objects.all())
        tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())


class TodoUserForm(UserCreationForm):
    telegram_id = forms.IntegerField(required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.telegram_id = self.cleaned_data["telegram_id"]
        if commit:
            print(f"Form User: {user}")
            user.save()
            print(f"Form Saved User: {user}")

        return user

    class Meta:
        model = User
        fields = ("username", "telegram_id", "password1", "password2")
