import json

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
)

from .models import Tag, TodoItem, Account
from .forms import (
    TagForm,
    AccountForm,
    TodoItemForm,
    TodoUserForm,
)


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


def register(request):
    if request.method == "POST":
        user_form = TodoUserForm(request.POST)

        print(f"Is Bound: {user_form.is_bound}")
        print(f"Is Valid: {user_form.is_valid()}")
        print(f"Errors: {user_form.errors}")

        if user_form.is_valid():
            print("Form is valid")
            user = user_form.save()
            print(f"Saved User: {user}")
            account = Account.objects.create(usr=user)
            print(f"Created Account: {account}")
            account.save()
            print(f"Saved Account: {account}")
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("get_todoitems")

        print("Form is invalid")
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = TodoUserForm()
    return render(request=request,
                  template_name="registration/registration.html",
                  context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in as {username}.")
                return redirect("get_todoitems")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request=request,
                  template_name="registration/login.html",
                  context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("log_in")
