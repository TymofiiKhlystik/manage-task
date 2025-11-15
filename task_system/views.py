from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView

from task_system.forms import TaskForm, TeamForm, WorkerUpdateForm, WorkerRegisterForm
from task_system.models import Worker, Task, TaskType, Position, Team

@login_required
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


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_system/task_list.html"
    ordering = ["is_complete", "-priority"]
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search", "")

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_system/task_form.html'

    def get_success_url(self):
        return reverse_lazy('task-detail', args=[self.object.id])


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('task-detail', args=[self.object.id])


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    template_name = 'task_system/task_delete.html'


@login_required
def mark_task_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_complete = True
    task.save()
    return redirect(reverse('task-detail', args=[task.id]))


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    template_name = "task_system/team_list.html"


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'task_system/team_form.html'


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    success_url = reverse_lazy('team-list')
    template_name = "task_system/team_detail.html"


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy('team-detail', args=[self.object.id])


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    template_name = "task_system/team_delete.html"
    success_url = reverse_lazy("team-list")


class WorkerList(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "task_system/worker_list.html"
    context_object_name = "worker_list"
    paginate_by = 10


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "task_system/worker_update.html"

    def get_object(self, queryset=None):
        # редагувати може лише сам себе
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("worker-list")


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = WorkerRegisterForm
    success_url = reverse_lazy("login")  # redirect after success

    def form_valid(self, form):
        user = form.save()
        # Якщо хочеш автологін після реєстрації → розкоментовуй ↓
        login(self.request, user)
        return super().form_valid(form)