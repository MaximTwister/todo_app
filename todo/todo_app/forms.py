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
    request_join_group = forms.CharField(max_length=50, required=False)
    telegram_id = forms.CharField()

    class Meta:
        model = Account
        fields = ['telegram_id']
        # TODO Create Group Drop-list (Andrew)

    def clean_telegram_id(self):
        telegram_id = self.cleaned_data.get('telegram_id')
        print(f"FORM TELEGRAM ID: {telegram_id} = {len(str(telegram_id))}")
        print(f"FORM CLEANED DATA: {self.cleaned_data}")
        if len(str(telegram_id)) != 10:
            raise forms.ValidationError('Not valid Telegram ID', code='invalid')

        # Always return a value to use as the new cleaned data,
        # even if this method didn't change it.
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


class TodoUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
