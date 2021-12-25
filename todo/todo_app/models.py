from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class TodoItem(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    assignee = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='assigned_todo_items')
    owner = models.ForeignKey(User,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='self_todo_items')
    tags = models.ManyToManyField('Tag',
                                  blank=False,
                                  related_name='todo_items')

    def __str__(self):
        return f'{self.owner}: {self.title}'

    def get_absolute_url(self):
        return reverse("get_todoitem", kwargs={"pk": self.pk})

    class Meta:
        db_table = 'todo_item'


class Account(models.Model):
    # default related name: TodoItem_set
    usr = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='account')
    telegram_id = models.BigIntegerField(blank=True, null=True)
    group = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.usr}: {self.group}: {self.telegram_id}'


class Tag(models.Model):
    title = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("get_todoitems", kwargs={"tag": self.title})
