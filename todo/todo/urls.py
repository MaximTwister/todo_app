from django.contrib import admin
from django.urls import path, include
from todo_app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("todo/", include("todo_app.urls")),
    path("register/", views.register, name="register"),
    path("login/", views.login_request, name="log_in"),
    path("logout/", views.logout_request, name="logout"),
    path("accounts/", include("django.contrib.auth.urls"))
]

