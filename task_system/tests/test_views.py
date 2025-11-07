from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from task_system.models import Task, TaskType, Position, Team


User = get_user_model()


class BaseViewTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="john",
            password="pass1234",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            position=self.position,
        )
        self.client.login(username="john", password="pass1234")


class IndexViewTest(BaseViewTest):
    def test_index_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_index_displays_stats(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_system/index.html")
        self.assertIn("num_workers", response.context)


class TaskListViewTest(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.task_type = TaskType.objects.create(name="Backend")
        self.team = Team.objects.create(name="Team A", description="Desc")
        self.task = Task.objects.create(
            name="Task 1",
            description="Testing",
            deadline=timezone.now(),
            task_type=self.task_type,
            team=self.team,
            priority=Task.Priority.HIGH,
        )

    def test_task_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 302)

    def test_task_list_renders(self):
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_system/task_list.html")
        self.assertContains(response, "Task 1")

    def test_search_filter(self):
        response = self.client.get(reverse("task-list"), {"search": "Task"})
        self.assertContains(response, "Task 1")
        response2 = self.client.get(reverse("task-list"), {"search": "Nope"})
        self.assertNotContains(response2, "Task 1")


class TaskCRUDTest(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.task_type = TaskType.objects.create(name="Frontend")
        self.team = Team.objects.create(name="Team X", description="Dev team")
        self.task = Task.objects.create(
            name="Old Task",
            description="Update me",
            deadline=timezone.now(),
            task_type=self.task_type,
            team=self.team,
            priority=Task.Priority.LOW,
        )

    def test_task_detail_view(self):
        response = self.client.get(reverse("task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_system/task_detail.html")

    def test_task_create_view(self):
        data = {
            "name": "New Task",
            "description": "Testing create",
            "deadline": timezone.now(),
            "task_type": self.task_type.id,
            "team": self.team.id,
            "priority": Task.Priority.HIGH,
        }
        response = self.client.post(reverse("task-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        data = {
            "name": "Updated Task",
            "description": "Edited",
            "deadline": timezone.now(),
            "task_type": self.task_type.id,
            "team": self.team.id,
            "priority": Task.Priority.URGENT,
        }
        response = self.client.post(reverse("task-update", args=[self.task.id]), data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_view(self):
        response = self.client.post(reverse("task-delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_mark_task_done(self):
        response = self.client.get(reverse("task-done", args=[self.task.id]))
        self.assertRedirects(response, reverse("task-detail", args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_complete)


class TeamCRUDTest(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.team = Team.objects.create(name="Team Alpha", description="For testing")

    def test_team_list_view(self):
        response = self.client.get(reverse("team-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Team Alpha")

    def test_team_create_view(self):
        data = {"name": "Team Bravo", "description": "New team"}
        response = self.client.post(reverse("team-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name="Team Bravo").exists())

    def test_team_update_view(self):
        data = {"name": "Team Zulu", "description": "Updated"}
        response = self.client.post(reverse("team-update", args=[self.team.id]), data)
        self.assertEqual(response.status_code, 302)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, "Team Zulu")

    def test_team_delete_view(self):
        response = self.client.post(reverse("team-delete", args=[self.team.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Team.objects.filter(id=self.team.id).exists())


class RegisterViewTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Manager")

    def test_register_creates_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "position": self.position.id,
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
