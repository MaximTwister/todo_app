from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from models import Tag


def get_tags(request: HttpRequest):
    tags = Tag.objects.get()
    context = {'tags': tags, 'title': "Tags List"}
    return render(request, 'todo_app/tags.html', context=context)
