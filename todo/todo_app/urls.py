from django.urls import path
import views

urlpatterns = [
    path('tags/', views.get_tags, name='get_tags')
]