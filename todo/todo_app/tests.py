from random import randint, choice
import english_words

from django.test import TestCase
from faker import Faker

from .models import Tag, TodoItem, User


fkr = Faker()


def create_users(users_amount=10):
    for _ in range(users_amount):
        User.objects.create(
            name=fkr.name(),
            telegram_id=randint(pow(10, 9), (pow(10, 10) - 1))
        )


def create_tags(tags_amount=10):
    words = english_words.english_words_lower_set
    for _ in range(tags_amount):
        Tag.objects.create(title=choice(list(words)))


def create_todos(todos_amount=10):
    title = fkr.sentence(nb_words=5)
    content = fkr.paragraph(nb_sentences=5)
    owner = choice(User.objects.all())
    assignee = owner
    while owner == assignee:
        assignee = choice(User.objects.all())


