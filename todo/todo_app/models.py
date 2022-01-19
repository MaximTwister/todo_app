from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class TodoItem(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_todo_items')
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='self_todo_items'
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        null=True,
        related_name='todo_items'
    )
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
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    telegram_id = models.BigIntegerField(blank=False, null=True)

    subscribed_groups = models.ManyToManyField(
        "Group",
        blank=True,
        related_name="subscribed_accounts"
    )
    usr = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="account"
    )

    def __str__(self):
        return f'{self.usr}: {self.subscribed_groups.all()}: {self.telegram_id}'


class Message(models.Model):
    text = models.TextField(max_length=200)
    message_date = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=20, default="info")
    acknowledged = models.BooleanField(default=False)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(
        max_length=50,
        blank=False,
        unique=True,
        verbose_name='Group'
    )
    accounts_want_to_subscribe = models.ManyToManyField(
        Account,
        blank=True,
        related_name="subscribe_requested_groups"
    )
    account_owner = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="own_groups"
    )

    def get_delete_url(self):
        return reverse("delete_group", kwargs={"pk": self.pk})

    def get_leave_url(self):
        return reverse("leave_group", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100,
                             blank=False,
                             verbose_name='Tag')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("get_todoitems_by_tag", kwargs={"tag": self.title})
