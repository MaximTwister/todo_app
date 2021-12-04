from django.urls import path

import todo_app.views as views

urlpatterns = [
    path('tags/', views.get_tags, name='get_tags'),
    path('users/', views.get_users, name='get_users'),
    path('todoitems/', views.get_todoitems, name='get_todoitems'),
]
