from django.urls import path

from task_system.views import index

urlpatterns = [
    path("", index, name="index"),WWWW
]