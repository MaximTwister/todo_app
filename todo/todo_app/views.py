import json

from django.views.generic import ListView, DetailView, DeleteView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tag, Account, TodoItem
from .forms import TodoUserForm


class TagsList(ListView):
    model = Tag


class TodoDetail(DetailView):
    model = TodoItem
    template_name = "todo_app/todoitem.html"
    context_object_name = "todoitem"

    def patch(self, request, *args, **kwargs):
        content_type = self.request.META.get("CONTENT_TYPE")
        if content_type == "application/json":
            pk = self.kwargs.get("pk")
            body = json.loads(self.request.body)
            todoitem = TodoItem.objects.get(pk=pk)
            todoitem.content = body.get("content")
            todoitem.title = body.get("title")
            todoitem.save()
        else:
            return JsonResponse(
                data={"error": f"ContentType: {content_type} is not supported"},
                status=405
            )
        return JsonResponse({'status': 200, 'message': "data updated"})


class TodoDelete(DeleteView):
    # DeleteView ONLY deletes on POST
    model = TodoItem
    success_url = reverse_lazy("get_todoitems")


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
