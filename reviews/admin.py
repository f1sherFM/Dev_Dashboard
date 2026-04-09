from django.contrib import admin

from .models import DailyReview


@admin.register(DailyReview)
class DailyReviewAdmin(admin.ModelAdmin):
    list_display = ("date", "mood", "energy_level", "focus_score", "overall_score")
    list_filter = ("mood", "date")
    search_fields = ("wins", "problems", "lessons", "tomorrow_plan")
    readonly_fields = ("created_at", "updated_at")
