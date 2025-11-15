from django.test import TestCase
from django.utils import timezone
from task_system.models import TaskType, Position, Worker, Team, Task


class TaskTypeModelTest(TestCase):
    def test_str_returns_name(self):
        ttype = TaskType.objects.create(name="Development")
        self.assertEqual(str(ttype), "Development")

    def test_ordering_by_name(self):
        TaskType.objects.create(name="B-type")
        TaskType.objects.create(name="A-type")
        names = list(TaskType.objects.values_list("name", flat=True))
        self.assertEqual(names, sorted(names))


class PositionModelTest(TestCase):
    def test_str_returns_name(self):
        pos = Position.objects.create(name="Manager")
        self.assertEqual(str(pos), "Manager")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Engineer")

    def test_str_returns_full_description(self):
        worker = Worker.objects.create_user(
            username="john",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            position=self.position,
            password="test1234"
        )
        self.assertIn("John - Doe", str(worker))
        self.assertIn("Engineer", str(worker))

    def test_worker_fields(self):
        worker = Worker.objects.create_user(
            username="maria",
            email="maria@example.com",
            first_name="Maria",
            last_name="Ivanova",
            position=self.position,
            password="test1234"
        )
        self.assertEqual(worker.email, "maria@example.com")
        self.assertEqual(worker.position.name, "Engineer")


class TeamModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="alice",
            email="alice@example.com",
            first_name="Alice",
            last_name="Cooper",
            position=self.position,
            password="pass1234"
        )

    def test_str_returns_name(self):
        team = Team.objects.create(name="QA Team", description="Test team")
        self.assertEqual(str(team), "QA Team")

    def test_workers_m2m_relationship(self):
        team = Team.objects.create(name="Dev Team", description="Development team")
        team.workers.add(self.worker)
        self.assertIn(self.worker, team.workers.all())


class TaskModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Backend")
        self.position = Position.objects.create(name="Engineer")
        self.worker = Worker.objects.create_user(
            username="john",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            position=self.position,
            password="test1234"
        )
        self.team = Team.objects.create(name="Team A", description="Alpha team")
        self.team.workers.add(self.worker)

    def test_create_task(self):
        task = Task.objects.create(
            name="API Work",
            description="Create API endpoints",
            deadline=timezone.now(),
            task_type=self.task_type,
            team=self.team,
            priority=Task.Priority.HIGH,
        )
        task.assignees.add(self.worker)

        self.assertEqual(task.name, "API Work")
        self.assertEqual(task.task_type.name, "Backend")
        self.assertIn(self.worker, task.assignees.all())
        self.assertEqual(task.team.name, "Team A")

    def test_priority_badge_class(self):
        task_high = Task(priority=Task.Priority.HIGH)
        task_low = Task(priority=Task.Priority.LOW)
        task_urgent = Task(priority=Task.Priority.URGENT)

        self.assertEqual(task_high.priority_badge_class(), "priority-high")
        self.assertEqual(task_low.priority_badge_class(), "priority-low")
        self.assertEqual(task_urgent.priority_badge_class(), "priority-urgent")
