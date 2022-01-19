from django.shortcuts import _get_queryset

from todo_app.models import Group, Account, Message


def request_subscribe_group(group_title, user):
    account = user.account
    query = {'title': group_title}
    group: Group = get_object_or_none(Group, **query)
    if not group:
        return False
    group.accounts_want_to_subscribe.add(user.account)
    Message.objects.create(
        text=f"{user.username} wants to join group {group}",
        account=group.account_owner
    )
    print("Subscription request was sent")
    return True


def is_requests_to_join(user):
    account = Account.objects.get(usr=user)
    groups = account.account_groups.all()
    for group in groups:
        if len(group.users_want_to_join.all()) > 0:
            return True
        else:
            return False


def get_object_or_none(query_class, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    query_class may be a Model, Manager, or QuerySet object. All others passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if
    more than one object is found.
    """
    queryset = _get_queryset(query_class)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def add_subscriber(account, group):
    account.subscribed_groups.add(group)
    account.save()
    group.accounts_want_to_subscribe.remove(account)
    Message.objects.create(
        text=f"You were added to group: {group}",
        severity="info",
        account=account
    )


def delete_subscriber(account, group):
    account.subscribed_groups.remove(group)
    account.save()
    Message.objects.create(
        text=f"You were deleted from group: {group}",
        severity="warning",
        account=account
    )


def reject_subscriber(account, group):
    group.accounts_want_to_subscribe.remove(account)
    Message.objects.create(
        text=f"Your request to join group: {group} was rejected",
        severity="warning",
        account=account
    )
