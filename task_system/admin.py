from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_system.models import Worker


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                    )
                },
            ),
        )
    )