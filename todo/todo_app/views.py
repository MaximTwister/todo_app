import json

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    login,
    logout,
    authenticate
)
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, resolve
from django.views.generic.edit import FormMixin, FormView
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView
)
from .models import (
    Tag,
    TodoItem,
    Account, Group, Message
)
from .forms import (
    TagForm,
    AccountForm,
    TodoItemForm,
    GroupForm, TodoUserForm
)
from .utils.common import (
    request_subscribe_group,
    add_subscriber,
    delete_subscriber,
    reject_subscriber,
)

TODO_TYPE_ALL = "todos"
TODO_TYPE_OWNER = "owner"
TODO_TYPE_ASSIGNEE = "assignee"

GROUP_TYPE_OWNED = "owned-groups"
GROUP_TYPE_SUBSCRIBER = "subscribed-groups"


class TodoDetail(LoginRequiredMixin, DetailView):
    model = TodoItem
    template_name = "todo_app/todoitem.html"
    login_url = reverse_lazy("log_in")
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


class MessageDetail(LoginRequiredMixin,DetailView):
    model = Message
    login_url = reverse_lazy("log_in")
    template_name = "todo_app/account.html"

    def get(self, request, *args, **kwargs):
        self.object: Message = self.get_object()
        self.object.acknowledged = True
        self.object.save()
        account_slug = self.request.user.account.slug
        return redirect(reverse_lazy("account", kwargs={'slug': account_slug}))


class GroupDetail(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "todo_app/todoitem.html"
    login_url = reverse_lazy("log_in")
    context_object_name = "groups"
    operation_method_map = {
        "add": add_subscriber,
        "del": delete_subscriber,
        "reject": reject_subscriber,
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        account = request.user.account
        current_url = resolve(request.path_info).url_name
        if current_url == "leave_group":
            account.subscribed_groups.remove(self.object)

        return redirect(reverse_lazy(
            "get_groups",
            kwargs={"group_type": "subscribed-groups"}
        ))

    def patch(self, request, *args, **kwargs):
        print(kwargs)
        content_type = request.META.get("CONTENT_TYPE")
        if content_type == "application/json":
            body = json.loads(request.body)
            operation_type = body.get("type")
            method = self.operation_method_map[operation_type]
            account_pk = body.get("account_pk")
            group_pk = self.kwargs.get("pk")
            group = Group.objects.get(pk=group_pk)
            account = Account.objects.get(pk=account_pk)
            method(account, group)
            return redirect(reverse_lazy(
                "get_groups",
                kwargs={'group_type': "owned-groups"}))

        else:
            return JsonResponse(data={"error": "not Supported method or content-type"},
                                status=405)


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    login_url = reverse_lazy("log_in")
    success_url = reverse_lazy("get_groups", kwargs={"group_type": "owned-groups"})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        account = self.object.account_owner
        self.object.delete()
        Message.objects.create(
            text=f"Your group: {self.object.title} was deleted",
            severity="warning",
            account=account
        )
        return HttpResponseRedirect(self.success_url)


class TodoDelete(LoginRequiredMixin, DeleteView):
    model = TodoItem
    login_url = reverse_lazy("log_in")
    success_url = reverse_lazy(
        "get_todoitems_by_type",
        kwargs={"todo_type": TODO_TYPE_ALL}
    )


class TodoItemsList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("log_in")
    redirect_field_name = reverse_lazy(
        "get_todoitems_by_type",
        kwargs={"todo_type": TODO_TYPE_ALL}
    )

    model = TodoItem
    template_name = "todo_app/todoitems.html"
    context_object_name = "todoitems"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.request.user.account
        context["groups"] = account.subscribed_groups.all()
        return context

    def get_queryset(self):
        filter_kwargs = {}
        todo_type = self.kwargs.get("todo_type")
        tag = self.kwargs.get("tag")
        account = self.request.user.account

        if todo_type in [TODO_TYPE_ALL, None]:
            owned_and_subscribed_groups = Group.objects.filter(
                Q(account_owner=account) |
                Q(subscribed_accounts__in=[account])
            )
            filter_kwargs["group__in"] = owned_and_subscribed_groups
        elif todo_type in [TODO_TYPE_OWNER, TODO_TYPE_ASSIGNEE]:
            filter_kwargs[todo_type] = self.request.user

        if tag:
            tag = Tag.objects.get(title=tag)
            filter_kwargs['tags'] = tag

        print(filter_kwargs)
        qs = super().get_queryset()
        return qs.filter(**filter_kwargs)


class GroupsList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("log_in")
    redirect_field_name = reverse_lazy(
        "get_groups",
        kwargs={"group_type": GROUP_TYPE_OWNED}
    )

    model = Group
    context_object_name = "groups"
    template_name = "todo_app/groups.html"
    include_template = None

    def get_queryset(self):
        group_type = self.kwargs["group_type"]
        group_type__options_map = {
            "owned-groups": [
                {"account_owner": self.request.user.account},
                "owned_group"
            ],
            "subscribed-groups": [
                {'subscribed_accounts': self.request.user.account},
                "subscribed_group"
            ]
        }
        filter_kwargs, self.include_template = group_type__options_map[group_type]
        print(f"Filter kwargs GroupList {filter_kwargs}")
        qs = super().get_queryset()
        print(f"Groups QuerySet: {qs}")
        return qs.filter(**filter_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["include_template"] = self.include_template
        return context


class AccountUpdate(LoginRequiredMixin, FormMixin, DetailView):
    model = Account
    template_name = "todo_app/account.html"
    login_url = reverse_lazy("log_in")
    form_class = AccountForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AccountForm(initial={
            "telegram_id": self.object.telegram_id,
        })
        context["subscribed_groups"] = self.object.subscribed_groups.all()
        context["account_messages"] = self.object.messages.filter(acknowledged=False)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        print(f"Form is_valid: {form.is_valid}")
        if form.is_valid():
            print(f"Form cleaned_data: {form.cleaned_data}")
            subscribe_group = form.cleaned_data.get("request_join_group")
            self.object.telegram_id = form.cleaned_data.get("telegram_id")
            self.object.save()
            if subscribe_group:
                subscribe_res = request_subscribe_group(subscribe_group, request.user)
                if not subscribe_res:
                    messages.error(request, f"Can not find group: {subscribe_group}")
                    return self.form_invalid(form)
            return super().form_valid(form)
        else:
            print(f"Form is not valid: {form.errors}")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("get_todoitems_by_type", kwargs={"todo_type": TODO_TYPE_ALL})


class GroupView(LoginRequiredMixin, FormView):
    template_name = 'todo_app/post_base.html'
    form_class = GroupForm
    login_url = reverse_lazy("log_in")
    success_url = reverse_lazy("get_groups", kwargs={'group_type': "owned-groups"})

    def form_valid(self, form):
        group: Group = form.save(commit=False)
        group.account_owner = self.request.user.account
        group.save()
        group.subscribed_accounts.add(self.request.user.account)
        return super().form_valid(form)


class CreateTodoItemView(LoginRequiredMixin, FormView):
    template_name = "todo_app/post_base.html"
    form_class = TodoItemForm
    login_url = reverse_lazy("log_in")
    success_url = reverse_lazy(
        "get_todoitems_by_type",
        kwargs={'todo_type': TODO_TYPE_OWNER}
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        print("Todo form is valid")
        todo_owner = self.request.user
        todo: TodoItem = form.save(commit=False)
        todo.owner = todo_owner
        todo.save()
        print("Todo form is saved")
        Message.objects.create(
            text=f"{todo_owner} assigned new todo for you.",
            account=todo.assignee.account
        )
        print("Message to assignee was send")
        return super().form_valid(form)


# TODO probably move to CBV (Anton)
def post_form(request, item):
    forms_mapping = {
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
        print(f"Form: {form}")
        owner = request.user
        if owner and form.is_valid():
            new_item = form.save()
            print(f"New Item: {new_item}")
            new_item.owner = owner
            new_item.save()
            return HttpResponseRedirect('?submitted=True')

    elif request.method == 'GET':
        if 'submitted' in request.GET:
            submitted = True

    context = {'form': form, 'submitted': submitted, 'title': title, 'tags': tags}
    return render(request, 'todo_app/post_base.html', context=context)


def get_assignees_by_group(request):
    if request.method == "PATCH":
        content_type = request.META.get("CONTENT_TYPE")
        if content_type == "application/json":
            account = request.user.account
            print(f"INFO: {request.body}")
            print(f"Account: {account}")
            body = json.loads(request.body)
            group_pk = body.get("group_pk")
            group: Group = Group.objects.get(pk=group_pk)
            assignees = group.subscribed_accounts.filter(~Q(pk=account.pk))
            assignees = {acc.usr.pk: acc.usr.username for acc in assignees}
            print(f"Assignees by group:{group} : {assignees}")
            return JsonResponse({"assignees": assignees}, status=200)
        else:
            return JsonResponse(data={"error": "Not Supported Method or ContentType"},
                                status=405)


def register(request):
    if request.method == "POST":
        user_form = TodoUserForm(request.POST)

        print(f"Is Bound: {user_form.is_bound}")
        print(f"Is Valid: {user_form.is_valid()}")
        print(f"Errors: {user_form.errors}")

        if user_form.is_valid():
            user = user_form.save()
            username = user.username
            account = Account.objects.create(
                slug=username,
                usr=user
            )
            account.save()
            login(request, user)
            messages.success(request, "Registration successful")
            todoitems_path = reverse_lazy(
                "get_todoitems_by_type",
                kwargs={"todo_type": TODO_TYPE_ALL}
            )
            return redirect(todoitems_path)

        print(f"Form is invalid: {user_form.errors}")
        messages.error(request, "Unsuccessful registration. Invalid info")

    print("Create ToDoUserForm")
    form = TodoUserForm()
    return render(request=request,
                  template_name="registration_templates/registration.html",
                  context={"register_form": form}
                  )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, f"Logged in as {username}")
                return redirect(reverse_lazy(
                    "get_todoitems_by_type",
                    kwargs={"todo_type": TODO_TYPE_ALL})
                )
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(
        request=request,
        template_name="registration_templates/login.html",
        context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect("log_in")
