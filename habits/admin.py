from django.contrib import admin

from .models import Habit, HabitEntry


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "frequency", "target_count", "unit", "is_active")
    list_filter = ("frequency", "is_active")
    search_fields = ("name", "slug", "description")
    readonly_fields = ("slug", "created_at", "updated_at")


@admin.register(HabitEntry)
class HabitEntryAdmin(admin.ModelAdmin):
    list_display = ("habit", "date", "value", "updated_at")
    list_filter = ("date", "habit")
    search_fields = ("habit__name", "note")
    autocomplete_fields = ("habit",)
