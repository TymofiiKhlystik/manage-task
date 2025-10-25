from django.urls import path

from task_system.views import (
    index,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    mark_task_done,
)


urlpatterns = [
    path("", index, name="index"),
    path("task_system/", TaskListView.as_view(), name="task-list"),
    path("task_system/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task_system/create/", TaskCreateView.as_view(), name="task-create"),
    path("task_system/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task_system/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path('task/<int:pk>/done/', mark_task_done, name='task-done'),

]