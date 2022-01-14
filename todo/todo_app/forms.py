from django import forms
from django.forms import ModelForm
from .models import Tag, TodoItem, Account,Group

from django.contrib.auth.models import User


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title']


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['group', 'telegram_id']
        widgets = {'group': forms.Select}
        group = forms.ModelChoiceField(queryset=Group.objects.all())
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
