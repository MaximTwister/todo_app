from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from todo_app.models import Tag, TodoItem


def get_tags(request: HttpRequest):
    tags = Tag.objects.get()
    context = {'tags': tags, 'title': "Tags List"}
    return render(request, 'todo_app/tags.html', context=context)


class BasedViewForTodoItems:

    @staticmethod
    def get_todo_items(request: HttpRequest):
        todo_items = TodoItem.objects.get()
        context = {'todo_items': todo_items, 'title': 'Todo Items List'}
        return render(request, 'todo_app/todo_items.html', context=context)


class BasedViewForUsers:

    @staticmethod
    def get_users(request: HttpRequest):
        users = TodoItem.objects.get()
        context = {'todo_items': users, 'title': 'Users List'}
        return render(request, 'todo_app/users.html', context=context)