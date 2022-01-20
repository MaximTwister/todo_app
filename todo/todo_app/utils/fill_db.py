from random import randint, choice

from faker import Faker
from django.db.models import Count, Q
from django.contrib.auth.models import User

from todo_app.models import Tag, TodoItem, Account, Group, Message
from todo_app.constants import all_tags as tags
from todo_app.constants import groups

fkr = Faker()

GROUP_TYPE_OWNER = "owner"
GROUP_TYPE_SUBSCRIBER = "subscriber"
FIRST_NAME = 0
SECOND_NAME = 1


def create_groups():
    groups_objects = []
    for group_title in groups:
        groups_objects.append(Group(title=group_title))
    Group.objects.bulk_create(groups_objects)


def get_group(group_max_participants, group_type, account=None):
    all_groups = Group.objects.annotate(num_participants=Count('subscribed_accounts'))
    if group_type == GROUP_TYPE_OWNER:
        groups_with_no_owners = all_groups.filter(account_owner__isnull=True)
        try:
            return choice(groups_with_no_owners)
        except IndexError:
            return list()
    if group_type == GROUP_TYPE_SUBSCRIBER:
        not_full_groups = all_groups.filter(
            Q(num_participants__lt=group_max_participants) &
            ~Q(account_owner=account) &
            ~Q(subscribed_accounts__in=[account])
        )
        return choice(not_full_groups)
    else:
        return list()


def get_group_to_subscribe_request(account):
    groups_to_subscribe = Group.objects.filter(
        ~Q(account_owner=account) &
        ~Q(accounts_want_to_subscribe__in=[account]) &
        ~Q(subscribed_accounts__in=[account])
    )
    try:
        return choice(groups_to_subscribe)
    except IndexError:
        return list()


def create_base_users(users_amount=10, groups_owner=3):
    for _ in range(users_amount):
        name_parts = fkr.name().split(" ")
        pretty_names = [name.lower().replace(".", "") for name in name_parts[:2]]
        username = "".join(pretty_names)
        password = "SuperStrongPass123"
        user = User.objects.create_user(
            first_name=name_parts[FIRST_NAME],
            last_name=name_parts[SECOND_NAME],
            username=username,
            password=password,
        )
        user.save()
        account = Account.objects.create(
            slug=username,
            telegram_id=fkr.numerify(text=('#' * 10)),
            usr=user,
        )
        print(f"\n[Account] created user: {user} with account: {account}")
        for _ in range(groups_owner):
            group = get_group(group_max_participants=5, group_type=GROUP_TYPE_OWNER)
            if not group:
                print("[Account] No groups without owners left. Skip.")
                break
            else:
                print(f"[Account: {username}] add own group: {group}")
                account.own_groups.add(group)
                account.subscribed_groups.add(group)


def add_additional_options_to_users(additional_groups_subscriber=3):
    accounts = Account.objects.all()
    for account in accounts:
        username = account.usr.username
        for _ in range(additional_groups_subscriber):
            group = get_group(group_max_participants=5,
                              group_type=GROUP_TYPE_SUBSCRIBER,
                              account=account)
            print(f"[Account: {username}] add additional subscription to group: {group}")
            account.subscribed_groups.add(group)
    for account in accounts:
        username = account.usr.username
        account_subscriptions = account.subscribed_groups.all()
        print(f"\n[Account: {username}] has subscriptions: {account_subscriptions}")
        create_todos(user=account.usr, subscribed_groups=account_subscriptions)

        for _ in range(additional_groups_subscriber):
            group_to_subscribe: Group = get_group_to_subscribe_request(account)
            print(f"[Account: {username}] requests group subscribe: {group_to_subscribe}")
            account.subscribe_requested_groups.add(group_to_subscribe)

            print(f"[Account: {username}] create message for group owner")
            subscribed_group_owner = group_to_subscribe.account_owner
            Message.objects.create(
                text=f"{username} wants to join group {group_to_subscribe}",
                account=subscribed_group_owner
        )


def create_tags():
    tags_objects = []
    for tag_title in tags:
        tags_objects.append(Tag(title=tag_title))
    Tag.objects.bulk_create(tags_objects)


def create_todos(user=None, subscribed_groups=None, todos_amount=10):
    tags_objects = Tag.objects.all()
    users_objects = User.objects.all()
    username = user.username

    for _ in range(todos_amount):

        if not user:
            user = choice(users_objects)
        if not subscribed_groups:
            subscribed_groups = choice(user.account.subscribed_groups.all())

        title = fkr.sentence(nb_words=5)
        content = fkr.paragraph(nb_sentences=5)
        assignee = user
        group = choice(subscribed_groups)
        while user == assignee:
            assignee = choice(users_objects)
        print(f"[Account: {username}] create todo in group: {group}")
        new_todoitem = TodoItem(
            title=title,
            content=content,
            owner=user,
            assignee=assignee,
            group=group
        )
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
    print("\nCreating Base Users and Accounts")
    create_base_users()
    print("\nAdding additional Options to Users and Accounts")
    add_additional_options_to_users()


if __name__ == "django.core.management.commands.shell":
    print("Start filling DB with data:\n")
    clear_old_data([Tag, Group, User, TodoItem])
    create_new_data()
