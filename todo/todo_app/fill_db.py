from random import randint, choice
import english_words

from django.test import TestCase
from faker import Faker

from .models import Tag, TodoItem, User
from .constants import all_tags

fkr = Faker()


def create_users(users_amount=10):
    for _ in range(users_amount):
        User.objects.create(
            name=fkr.name(),
            telegram_id=fkr.numerify(text=('#'*10)))


def update_tags():
    for tag in all_tags:
        if not list(Tag.objects.filter(title=tag)):
            Tag.objects.create(title=tag)


def create_todos(todos_amount=10):
    for _ in range(todos_amount):
        title = fkr.sentence(nb_words=5)
        content = fkr.paragraph(nb_sentences=5)
        owner = choice(User.objects.all())
        assignee = owner
        while owner == assignee:
            assignee = choice(User.objects.all())
        new_user = TodoItem(title=title, content=content, owner=owner, assignee=assignee)
        new_user.save()
        for _ in range(randint(1, 4)):
            new_user.tags.add(choice(Tag.objects.all()))
