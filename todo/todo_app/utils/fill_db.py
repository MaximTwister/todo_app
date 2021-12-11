from random import randint, choice

from faker import Faker

from todo.todo_app.models import Tag, TodoItem, User
from todo.todo_app.constants import all_tags as tags


fkr = Faker()


def create_users(users_amount=10):
    for _ in range(users_amount):
        User.objects.create(
            name=fkr.name(),
            telegram_id=fkr.numerify(text=('#' * 10)))


def update_tags():
    exist_tags = list(Tag.objects.values_list("title", flat=True))
    new_tags = [Tag(title=tag) for tag in tags if tag not in exist_tags]
    Tag.objects.bulk_create(new_tags)


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
