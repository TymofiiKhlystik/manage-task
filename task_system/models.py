from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
            return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers"
    )
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return (
            f"{self.first_name} - {self.last_name} > "
            f"Position: {self.position.name}"
        )



class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    workers = models.ManyToManyField(Worker, related_name="teams")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("team-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "urgent", "Urgent"
        HIGH = "high", "High"
        LOW = "low", "Low"
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(Worker, blank=True, related_name="assignees")
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    def priority_badge_class(self):
        return {
            self.Priority.URGENT: "priority-urgent",
            self.Priority.HIGH: "priority-high",
            self.Priority.LOW: "priority-low",
        }.get(self.priority, "priority-low")
