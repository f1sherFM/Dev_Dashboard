from django.contrib import admin

from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "status", "priority", "deadline", "is_archived")
    list_filter = ("type", "status", "priority", "is_archived")
    search_fields = ("title", "slug", "description")
    readonly_fields = ("slug", "created_at", "updated_at", "completed_at")
