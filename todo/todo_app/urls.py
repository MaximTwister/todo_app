from django.urls import path

import todo_app.views as views

urlpatterns = [
    path('tags/', views.get_tags, name='get_tags'),
    path('users/', views.get_users, name='get_users'),
    path("todoitems/", views.TodoItemsList.as_view(), name='get_todoitems'),
    path("todoitems/<str:tag>/", views.TodoItemsList.as_view(), name='get_todoitems'),
    path('todoitem/<int:pk>/', views.TodoDetail.as_view(), name='get_todoitem'),
    path("todoitem/<int:pk>/update/", views.TodoUpdate.as_view(), name='update_todoitem'),
    path("todoitem/<int:pk>/delete/", views.TodoDelete.as_view(), name='delete_todoitem'),
]
