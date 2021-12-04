from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from . import models


def get_tags(request: HttpRequest):
    tags = models.Tag.objects.all()
    context = {'tags': tags, 'title': "Tags List"}
    return render(request, 'todo_app/tags.html', context=context)


def get_todo_items(request: HttpRequest):
    todo_item = models.TodoItem.objects.all()
    context = {'todo_item': todo_item, 'title': "Todo_items List"}
    return render(request, 'todo_app/todo_items.html', context=context)


def get_users(request: HttpRequest):
    user = models.User.objects.all()
    context = {'user': user, 'title': "Users List"}
    return render(request, 'todo_app/users.html', context=context)

