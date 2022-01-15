from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Tag, TodoItem, Account, Group


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title']


class AccountForm(ModelForm):
    telegram_id = forms.CharField(max_length=10, required=False)
    request_join_group = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Account
        fields = ['telegram_id']
        # widgets = {'account_groups': forms.Select}

    def clean_telegram_id(self):
        telegram_id = self.cleaned_data.get('telegram_id')
        if len(str(telegram_id)) != 10:
            raise forms.ValidationError('not valid telegram id', code='invalid')

        # Must always return data
        return telegram_id


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


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title']
        title = forms.CharField(max_length=255)


class TodoUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
