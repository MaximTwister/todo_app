import json

from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tag, Account, TodoItem
from .forms import TodoUserForm


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


class TodoDetailView(DetailView):
    model = TodoItem
    template_name = "todo_app/todoitem.html"
    context_object_name = "todoitem"


@login_required(login_url="/login/")
def get_todoitems(request: HttpRequest, tag=None):
    if tag:
        todoitems = TodoItem.objects.filter(tags__title=tag)
    else:
        todoitems = TodoItem.objects.all()
    context = {'todoitems': todoitems,
               'title': 'TodoItems list'
               }
    return render(request, 'todo_app/todoitems.html', context=context)


class TagsList(ListView):
    model = Tag


class TodoItemsList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    model = TodoItem
    template_name = "todo_app/todoitems.html"
    context_object_name = "todoitems"

    def get_queryset(self):
        filter_kwargs = {"owner": self.request.user}
        if "tag" in self.kwargs:
            tag_title = self.kwargs.get("tag")
            tag = Tag.objects.get(title=tag_title)
            filter_kwargs['tags'] = tag
        print(filter_kwargs)
        qs = super().get_queryset()
        return qs.filter(**filter_kwargs)


def update_todoitem(request, pk):
    # request.is_ajax deprecated since django 3.1
    is_ajax = request.META.get("CONTENT_TYPE") == "application/json"
    if is_ajax and request.method == "POST":
        body = json.loads(request.body)
        print(f"AJAX Request Body : {body}")
        todoitem = TodoItem.objects.get(pk=pk)
        todoitem.content = body.get("content")
        todoitem.title = body.get("title")
        todoitem.save()
    else:
        return JsonResponse(data={"error": "Not supported Method"}, status=405)
    return JsonResponse({'foo': 'bar'})




def register(request):
    if request.method == "POST":
        user_form = TodoUserForm(request.POST)

        print(f"Is Bound: {user_form.is_bound}")
        print(f"Is Valid: {user_form.is_valid()}")
        print(f"Errors: {user_form.errors}")

        if user_form.is_valid():
            print("Form is valid")
            user = user_form.save()
            account = Account.objects.create(usr=user)
            account.save()
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
