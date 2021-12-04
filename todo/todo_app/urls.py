from django.urls import path
from . import views

urlpatterns = [
    path('tags/', views.get_tags, name='get_tags'),
    path('todoitems/', views.get_todo_items, name='get_todoitems'),
    path('users/', views.get_users, name='get_users')
]