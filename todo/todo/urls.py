from django.contrib import admin
from django.urls import path, include
from todo_app import views


urlpatterns = [
    path("", views.login_request, name="log_in"),
    path("admin/", admin.site.urls),
    path("todo/", include("todo_app.urls")),
    path("register/", views.register, name="register"),
    path("login/", views.login_request, name="log_in"),
    path("logout/", views.logout_request, name="log_out"),
    path("account/<slug:slug>/", views.AccountUpdate.as_view(), name="account"),
]

