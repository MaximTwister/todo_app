from random import randint, choice

from django.db.models import Count
from faker import Faker
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from todo_app.models import Tag, TodoItem, Account, Group
from todo_app.constants import all_tags as tags

fkr = Faker()


def create_groups():
    group_titles = ("Alpha", "Bravo", "Charlie", "Delta",
                    "Echo", "Foxtrot", "Golf", "Hotel",)
    groups_objects = []
    for group_title in group_titles:
        try:
            Group.objects.get(title=group_title)
            print(f"Group {group_title} already exist")
            continue
        except ObjectDoesNotExist:
            groups_objects.append(Group(title=group_title))
    Group.objects.bulk_create(groups_objects)


def get_not_full_group(group_max_participants):
    all_groups = Group.objects.annotate(num_participants=Count('accounts'))
    not_full_groups = all_groups.filter(num_participants__lt=group_max_participants)
    if not_full_groups:
        return choice(not_full_groups)
    else:
        print("All groups are fully staffed.")
        return list()


def create_users(users_amount=100):
    for _ in range(users_amount):
        first_name, last_name, *_ = fkr.name().split(" ")
        username = " ".join([first_name.lower(), last_name.lower()])
        password = "SuperStrongPass123"
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
        user.save()
        account = Account.objects.create(
            telegram_id=fkr.numerify(text=('#' * 10)),
            usr=user,
        )
        group = get_not_full_group(group_max_participants=5)
        if group:
            account.account_groups.add()
        else:
            print("No empty groups left. Stop creating users. Exit")
            break


def update_tags():
    exist_tags = list(Tag.objects.values_list("title", flat=True))
    new_tags = [Tag(title=tag) for tag in tags if tag not in exist_tags]
    Tag.objects.bulk_create(new_tags)


def create_todos(todos_amount=100):
    tags_objects = Tag.objects.all()
    users_objects = User.objects.all()
    for _ in range(todos_amount):
        title = fkr.sentence(nb_words=5)
        content = fkr.paragraph(nb_sentences=5)
        owner = choice(users_objects)
        assignee = owner
        while owner == assignee:
            assignee = choice(users_objects)
        new_todoitem = TodoItem(title=title, content=content, owner=owner,
                                assignee=assignee)
        new_todoitem.save()
        for _ in range(randint(1, 4)):
            new_todoitem.tags.add(choice(tags_objects))
