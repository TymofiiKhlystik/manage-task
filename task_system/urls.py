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
    path("list/", TaskListView.as_view(), name="task-list"),
    path("task_detail/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task_create/create/", TaskCreateView.as_view(), name="task-create"),
    path("task_update/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task_delete/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path('task/<int:pk>/done/', mark_task_done, name='task-done'),

]