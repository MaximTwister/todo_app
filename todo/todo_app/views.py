from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from .models import Tag, User, TodoItem
from .forms import TagForm, UserForm, TodoItemForm


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


def post_form(request, item):
    forms = {'user': {'title': 'Create user', 'form': UserForm},
             'tag': {'title': 'Create tag', 'form': TagForm},
             'todoitem': {'title': 'Create todoitem', 'form': TodoItemForm}}

    title = forms[item]['title']
    submitted = False
    if request.method == 'POST':
        form = forms[item]['form'](request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?submitted=True')

    else:
        form = forms[item]['form']
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'todo_app/post_base.html', {'form': form,
                                                       'submitted': submitted,
                                                       'title': title})





