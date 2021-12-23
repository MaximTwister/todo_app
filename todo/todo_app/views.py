import json

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tag, User, TodoItem
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
    return redirect("login")
