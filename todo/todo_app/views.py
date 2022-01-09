import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from .models import Tag, Account, TodoItem
from .forms import TagForm, AccountForm, TodoItemForm


class TodoDetail(DetailView):
    model = TodoItem
    template_name = "todo_app/todoitem.html"
    context_object_name = "todoitem"

    def patch(self, request, *args, **kwargs):
        print(kwargs)
        content_type = request.META.get("CONTENT_TYPE")
        if content_type == "application/json":
            pk = self.kwargs.get("pk")
            body = json.loads(request.body)
            todoitem = TodoItem.objects.get(pk=pk)
            todoitem.content = body.get("content")
            todoitem.title = body.get("title")
            todoitem.save()
            return JsonResponse({"status": "Updated"}, status=200)
        else:
            return JsonResponse(data={"error": "Not Supported Method or ContentType"},
                                status=405)


class TodoDelete(DeleteView):
    model = TodoItem
    success_url = reverse_lazy("get_todoitems")


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


# TODO probably move to CBV (Anton)
def post_form(request, item):
    forms_mapping = {
        'user': ('Create user', AccountForm),
        'tag': ('Create tag', TagForm),
        'todoitem': ('Create todoitem', TodoItemForm),
    }

    title, form = forms_mapping[item]
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
