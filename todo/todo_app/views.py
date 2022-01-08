import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView

from .models import Tag, User, TodoItem
from .forms import TagForm, UserForm, TodoItemForm


def get_tags(request: HttpRequest):
    tags = Tag.objects.all()
    context = {'tags': tags,
               'title': 'Tags list'
               }
    return render(request, 'todo_app/tags.html', context=context)


class TagsList(ListView):
    model = Tag


def get_users(request: HttpRequest):
    users = User.objects.all()
    context = {'users': users,
               'title': 'Users list'
               }
    return render(request, 'todo_app/users.html', context=context)


class TodoDetailView(DetailView):
    model = TodoItem
    template_name = "todo_app/todoitem.html"
    context_object_name = "todoitem"


class TodoItemsList(ListView):
    model = TodoItem
    template_name = "todo_app/todoitems.html"
    context_object_name = "todoitems"

    def get_queryset(self):
        filter_kwargs = {}
        if "tag" in self.kwargs:
            tag_title = self.kwargs.get("tag")
            tag = Tag.objects.get(title=tag_title)
            filter_kwargs['tags'] = tag
        print(filter_kwargs)
        qs = super().get_queryset()
        return qs.filter(**filter_kwargs)



def post_form(request, item):
    forms = {
        'user': ('Create user', UserForm),
        'tag': ('Create tag', TagForm),
        'todoitem': ('Create todoitem', TodoItemForm),
    }

    title, form = forms[item]
    if title == 'Create todoitem':
        tags = Tag.objects.all()
    else:
        tags = []
    submitted = False

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?submitted=True')

    elif request.method == 'GET':
        if 'submitted' in request.GET:
            submitted = True

    context = {'form': form, 'submitted': submitted, 'title': title, 'tags': tags}
    return render(request, 'todo_app/post_base.html', context=context)


def update_todoitem(request, pk):
    is_json = request.META.get("CONTENT_TYPE") == "application/json"
    if is_json and request.method == "POST":
        body = json.loads(request.body)
        todoitem = TodoItem.objects.get(pk=pk)
        todoitem.content = body.get("content")
        todoitem.title = body.get("title")
        todoitem.save()
        return JsonResponse({"status": "Updated"}, status=200)
    else:
        return JsonResponse(data={"error": "Not Supported Method or ContentType"}, status=405)
