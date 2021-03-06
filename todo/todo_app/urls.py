from django.urls import path

import todo_app.views as views

urlpatterns = [
    path('todoitem/<int:pk>/', views.TodoDetail.as_view(), name='get_todoitem'),
    path('todoitem/<int:pk>/update/', views.TodoDetail.as_view(), name='update_todoitem'),
    path('todoitem/<int:pk>/delete/', views.TodoDelete.as_view(), name='delete_todoitem'),
    path("todoitems/", views.TodoItemsList.as_view(), name='get_todoitems'),
    path("todoitems/<str:tag>/", views.TodoItemsList.as_view(), name='get_todoitems'),
    path("create_form/<str:item>/", views.post_form, name='post_form')
]
