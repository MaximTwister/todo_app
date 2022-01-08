from django.db import models
from django.urls import reverse


class TodoItem(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    assignee = models.ForeignKey('User',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='assigned_todo_items')
    owner = models.ForeignKey('User',
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


class User(models.Model):
    # default related name: TodoItem_set
    name = models.CharField(max_length=50, blank=False)
    telegram_id = models.BigIntegerField(blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}: {self.telegram_id}'


# TODO tags MUST be unique (Andrew)
class Tag(models.Model):
    title = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("get_todoitems", kwargs={"tag": self.title})
