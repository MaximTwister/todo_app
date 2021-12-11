from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Tag, User, TodoItem


def get_tags(request: HttpRequest):
    tags = Tag.objects.all()
    context = {'tags': tags,
               'title': 'Tags list'
               }
    return render(request, 'todo_app/tags.html', context=context)


def get_users(request: HttpRequest):
    users = User.objects.all()
    context = {'users': users,
               'title': 'Users list'
               }
    return render(request, 'todo_app/users.html', context=context)


def get_todoitem(request, pk):
    todoitem = TodoItem.objects.get(pk=pk)
    context = {'todoitem': todoitem,
               'title': F"TodoItem {todoitem.title}",
               "read_mode": True,
               }
    return render(request, 'todo_app/todoitems.html', context=context)


def get_todoitems(request: HttpRequest, tag=None):
    if tag:
        todoitems = TodoItem.objects.filter(tags__title=tag)
    else:
        todoitems = TodoItem.objects.all()
    context = {'todoitems': todoitems,
               'title': 'TodoItems list'
               }
    return render(request, 'todo_app/todoitems.html', context=context)
