from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from todo_app.models import Tag, User, TodoItem


def get_tags(request: HttpRequest):
    tags = Tag.objects.get()
    context = {'tags': tags,
               'title': 'Tags list'
               }
    return render(request, 'todo_app/tags.html', context=context)


def get_users(request: HttpRequest):
    users = User.objects.get()
    context = {'users': users,
               'title': 'Users list'
               }
    return render(request, 'todo_app/users.html', context=context)


def get_todoitems(request: HttpRequest):
    todoitems = TodoItem.objects.get()
    context = {'todoitems': todoitems,
               'title': 'TodoItems list'
               }
    return render(request, 'todo_app/todoitems.html', context=context)


