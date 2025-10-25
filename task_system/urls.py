from django.urls import path

from task_system.views import (
    index,
    TaskListView,
    TaskDetailView,
)


urlpatterns = [
    path("", index, name="index"),
    path("task_system/", TaskListView.as_view(), name="task-list"),
    path("task_system/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),

]