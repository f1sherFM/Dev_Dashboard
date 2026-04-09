from django.contrib import admin

from .models import ProjectSnapshot


@admin.register(ProjectSnapshot)
class ProjectSnapshotAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "is_active", "started_at", "last_updated")
    list_filter = ("status", "is_active")
    search_fields = ("name", "slug", "description", "current_focus", "next_step")
    readonly_fields = ("slug", "created_at", "updated_at")
