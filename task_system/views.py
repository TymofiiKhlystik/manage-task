from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from task_system.models import Worker, Task, TaskType, Position


def index(request: HttpRequest) -> HttpResponse:
    num_workers = Worker.objects.all().count()
    num_tasks = Task.objects.all().count()
    num_completed_tasks = Task.objects.filter(is_complete=True).count()
    num_type_tasks = TaskType.objects.all().count()
    num_position = Position.objects.all().count()
    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_completed_tasks": num_completed_tasks,
        "num_type_tasks": num_type_tasks,
        "num_position": num_position,
    }
    return render(request, "task_system/index.html", context=context)


class TaskListView(generic.ListView):
    model = Task
    template_name = "task_system/task_list.html"
    ordering = ["is_complete", "-priority"]


class TaskDetailView(generic.DetailView):
    model = Task