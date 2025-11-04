from django.urls import path

from task_system.models import Worker
from task_system.views import (
    index,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    mark_task_done,
    TeamListView,
    TeamCreateView,
    TeamDetailView,
    TeamUpdateView,
    TeamDeleteView,
    WorkerList,
    WorkerUpdateView,
    RegisterView,
)


urlpatterns = [
    # ---- TASKS ----
    path("", index, name="index"),
    path("list/", TaskListView.as_view(), name="task-list"),
    path("task_detail/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task_create/create/", TaskCreateView.as_view(), name="task-create"),
    path("task_update/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task_delete/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path('task/<int:pk>/done/', mark_task_done, name='task-done'),
    # ---- TEAMS ----
    path('teams/', TeamListView.as_view(), name="team-list"),
    path('team/create/', TeamCreateView.as_view(), name="team-create"),
    path('team/<int:pk>/', TeamDetailView.as_view(), name="team-detail"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
    # ----WORKERS----
    path("workers/", WorkerList.as_view(), name="worker-list"),
    path("workers/update/", WorkerUpdateView.as_view(), name="worker-update"),
    # ----REGISTER----
    path("register/", RegisterView.as_view(), name="register"),
]