from random import randint, choice

from faker import Faker
from django.db.models import Count, Q
from django.contrib.auth.models import User

from todo_app.models import Tag, TodoItem, Account, Group
from todo_app.constants import all_tags as tags
from todo_app.constants import groups

fkr = Faker()


def create_groups():
    groups_objects = []
    for group_title in groups:
        groups_objects.append(Group(title=group_title))
    Group.objects.bulk_create(groups_objects)


def get_not_full_group(group_max_participants):
    all_groups = Group.objects.annotate(num_participants=Count('subscribed_accounts'))
    not_full_groups = all_groups.filter(num_participants__lt=group_max_participants)
    no_owners_groups = all_groups.filter(account_owner__isnull=True)
    if no_owners_groups:
        return "owner", choice(no_owners_groups)
    elif not_full_groups:
        return "subscriber", choice(not_full_groups)
    else:
        return list()


def get_group_to_subscribe(account):
    groups_to_subscribe = Group.objects.filter(
        ~Q(account_owner=account) &
        ~Q(accounts_want_to_subscribe__in=[account]) &
        ~Q(subscribed_accounts__in=[account])
    )
    return groups_to_subscribe


def create_users(users_amount=10):
    for user_index in range(users_amount):
        first_name, last_name, *_ = fkr.name().split(" ")
        username = "".join([first_name.lower(), last_name.lower()])
        password = "SuperStrongPass123"
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
        user.save()
        account = Account.objects.create(
            slug=username,
            telegram_id=fkr.numerify(text=('#' * 10)),
            usr=user,
        )
        group_type, group = get_not_full_group(group_max_participants=5)
        if group_type == "owner":
            print("[Account] add own group")
            account.own_groups.add(group)
        elif group_type == "subscriber":
            print("[Account] add subscription to group")
            account.subscribed_groups.add(group)
        else:
            User.objects.get(user).delete()
            print("No empty groups left. Stop creating users. Exit")
            break

        if user_index > 0:
            print("[Account] creating Todos")
            create_todos(user=user, group=group)
            groups_to_subscribe = get_group_to_subscribe(account)
            if groups_to_subscribe:
                print("[Account] add subscribe requests to the Group\n")
                account.subscribe_requested_groups.add(choice(groups_to_subscribe))
            else:
                print("[Account] No eligible groups to subscribe")


def create_tags():
    tags_objects = []
    for tag_title in tags:
        tags_objects.append(Tag(title=tag_title))
    Tag.objects.bulk_create(tags_objects)


def create_todos(user=None, group=None, todos_amount=10):
    tags_objects = Tag.objects.all()
    users_objects = User.objects.all()
    for _ in range(todos_amount):
        if not user:
            user = choice(users_objects)
        if not group:
            group = user.account.own_groups.all().first()
        title = fkr.sentence(nb_words=5)
        content = fkr.paragraph(nb_sentences=5)
        assignee = user
        while user == assignee:
            assignee = choice(users_objects)
        new_todoitem = TodoItem(title=title, content=content, owner=user,
                                assignee=assignee, group=group)
        new_todoitem.save()
        for _ in range(randint(1, 4)):
            new_todoitem.tags.add(choice(tags_objects))


def clear_old_data(models_list):
    for model in models_list:
        print(f"[{model.__name__}] Clear all data")
        model.objects.all().delete()


def create_new_data():
    print("\nCreating Groups")
    create_groups()
    print("\nCreating Tags")
    create_tags()
    print("\nCreating Users and Accounts")
    create_users()


if __name__ == "django.core.management.commands.shell":
    print("Start filling DB with data:\n")
    clear_old_data([Tag, Group, User, TodoItem])
    create_new_data()
