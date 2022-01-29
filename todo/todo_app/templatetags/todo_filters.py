from django import template

from todo_app.models import Message

register = template.Library()


@register.filter
def get_unread_messages_num(account_messages: Message.objects):
    """Get an amount of account unacknowledged messages"""
    return len(account_messages.filter(acknowledged=False))
