from django import forms
from django.forms import ModelForm
from .models import Tag, TodoItem, User


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'telegram_id']
        widgets = {'name': forms.Textarea(attrs={'rows': 2})}
        name = forms.CharField()
        telegram_id = forms.IntegerField()

    def clean_telegram_id(self):
        telegram = self.cleaned_data.get('telegram_id')
        if len(str(telegram)) != 10:
            raise forms.ValidationError('You must enter a valid telegram id', code='invalid')


class CustomChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return user.name


class TodoItemForm(ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'content',  'owner', 'assignee', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
            'title': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea
        }
        field_classes = {'owner': CustomChoiceField, 'assignee': CustomChoiceField}
        title = forms.CharField()
        content = forms.CharField()
        owner = forms.ModelChoiceField(queryset=User.objects.all())
        assignee = CustomChoiceField(queryset=User.objects.all())
        tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
