from django.urls import path

import todo_app.views as views

urlpatterns = [
    path('todoitem/<int:pk>/', views.TodoDetail.as_view(), name='get_todoitem'),
    path('todoitem/<int:pk>/update/', views.TodoDetail.as_view(), name='update_todoitem'),
    path('todoitem/<int:pk>/delete/', views.TodoDelete.as_view(), name='delete_todoitem'),
    path("todoitems/<str:todo_type>/", views.TodoItemsList.as_view(), name='get_todoitems_by_type'),
    path("todoitems/<str:tag>/", views.TodoItemsList.as_view(), name='get_todoitems_by_tag'),
    path("groups/<int:pk>/update/", views.GroupDetail.as_view(), name="edit_group"),
    path("groups/<int:pk>/delete/", views.GroupDelete.as_view(), name="delete_group"),
    path("groups/<int:pk>/leave/", views.GroupDetail.as_view(), name="leave_group"),
    path("groups/<str:group_type>/", views.GroupsList.as_view(), name='get_groups'),
    path("create_group/", views.GroupView.as_view(), name='create_group'),
    path("create_form/todoitem/", views.CreateTodoItemView.as_view(), name='todoitem_form'),
    path("create_form/<str:item>/", views.post_form, name='post_form'),
    path("message/<int:pk>/", views.MessageDetail.as_view(), name='message_detail'),

]
