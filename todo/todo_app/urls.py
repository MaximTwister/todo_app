from django.urls import path

import todo_app.views as views

urlpatterns = [
    path('tags/', views.get_tags, name='get_tags'),
    path('users/', views.get_users, name='get_users'),
    path('todoitem/<int:pk>/', views.TodoDetailView.as_view(), name='get_todoitem'),
    path('todoitem/<int:pk>/update/', views.update_todoitem, name='update_todoitem'),
    path("todoitems/", views.TodoItemsList.as_view(), name='get_todoitems'),
    path("todoitems/<str:tag>/", views.TodoItemsList.as_view(), name='get_todoitems'),
    path("create_form/<str:item>/", views.post_form, name='post_form')
]
