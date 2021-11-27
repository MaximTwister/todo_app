from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest):
    print(f"Request: {request}")
    return HttpResponse("Hello From Django")
