from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm

from .models import Tag, TodoItem, Account, Group


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        widgets = {'title': forms.Textarea(attrs={'rows': 1, 'cols': 36})}


class AccountForm(ModelForm):
    telegram_id = forms.CharField(max_length=10, required=False)
    request_join_group = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Account
        fields = ['telegram_id', 'request_join_group']
        # widgets = {'account_groups': forms.Select}

    def clean_telegram_id(self):
        telegram_id = self.cleaned_data.get('telegram_id')
        if len(str(telegram_id)) not in range(9, 11):
            raise forms.ValidationError('not valid telegram id', code='invalid')

        # Must always return data
        return telegram_id


class CustomChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return user.username


class TodoItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            user_groups = Group.objects.filter(subscribed_accounts=user.account)
            user_groups_ids = [group.id for group in user_groups]
            assignee = User.objects.filter(
                Q(account__subscribed_groups__in=user_groups_ids) &
                ~Q(pk=user.pk)
            ).distinct()
            # assignee = User.objects.filter(username="")
            print(f"[{user}] Available groups for todo form : {user_groups}")
            print(f"[{user}] Available assignees for todo form: {assignee}")
            self.fields['group'].queryset = user_groups
            self.fields['assignee'].queryset = assignee

    class Meta:
        model = TodoItem
        fields = ['title', 'content', 'assignee', 'group', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'tag_widget'}),
            'title': forms.Textarea(attrs={'rows': 1, 'cols': 36}),
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 36})
        }
        field_classes = {'assignee': CustomChoiceField}
        title = forms.CharField()
        content = forms.CharField()
        tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title']
        title = forms.CharField(max_length=255)
        widgets = {'title': forms.Textarea(attrs={'rows': 1, 'cols': 36})}


class TodoUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
