from django.urls import path

from task_system.views import index, TaskListView

urlpatterns = [
    path("", index, name="index"),
    path("list-tasks/", TaskListView.as_view(), name="list-tasks"),
]