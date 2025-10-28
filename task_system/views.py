from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_system.forms import TaskForm
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
    paginate_by = 2


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_system/task_form.html'

    def get_success_url(self):
        return reverse_lazy('task-detail', args=[self.object.id])


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('task-detail', args=[self.object.id])


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    template_name = 'task_system/task_delete.html'

def mark_task_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_complete = True
    task.save()
    return redirect(reverse('task-detail', args=[task.id]))