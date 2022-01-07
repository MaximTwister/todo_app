from random import randint, choice

from faker import Faker
from django.contrib.auth.models import User

from todo_app.models import Tag, TodoItem, Account
from todo_app.constants import all_tags as tags


fkr = Faker()


def create_users(users_amount=10):
    for _ in range(users_amount):
        first_name, second_name, *_ = fkr.name().split(" ")
        username = "".join([first_name.lower(), second_name.lower()])
        password = "SuperStrongPass123"
        user = User.objects.create_user(
            first_name=first_name,
            last_name=second_name,
            username=username,
            password=password)
        user.save()
        account = Account.objects.create(usr=user)
        account.save()
    # telegram_id=fkr.numerify(text=('#' * 10)))


def update_tags():
    exist_tags = list(Tag.objects.values_list("title", flat=True))
    new_tags = [Tag(title=tag) for tag in tags if tag not in exist_tags]
    Tag.objects.bulk_create(new_tags)


def create_todos(todos_amount=10, predefined_owner_pk=None):
    tags_objects = Tag.objects.all()
    users_objects = User.objects.all()
    for _ in range(todos_amount):
        title = fkr.sentence(nb_words=5)
        content = fkr.paragraph(nb_sentences=5)
        if not predefined_owner_pk:
            owner = choice(users_objects)
        else:
            owner = users_objects.get(pk=predefined_owner_pk)
        assignee = owner
        while owner == assignee:
            assignee = choice(users_objects)
        new_user = TodoItem(title=title, content=content, owner=owner, assignee=assignee)
        new_user.save()
        for _ in range(randint(1, 4)):
            new_user.tags.add(choice(tags_objects))


def main():
    create_users()
    update_tags()
    create_todos()
