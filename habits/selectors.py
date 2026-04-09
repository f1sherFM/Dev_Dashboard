from datetime import date

from django.db.models import Prefetch

from .models import Habit, HabitEntry


def get_habits_for_list():
    return Habit.objects.prefetch_related(
        Prefetch("entries", queryset=HabitEntry.objects.order_by("-date", "-updated_at"))
    )


def get_habit_by_slug(slug):
    return Habit.objects.filter(slug=slug)


def get_recent_entries_for_habit(habit, limit=7):
    return habit.entries.order_by("-date", "-updated_at")[:limit]


def get_habit_detail_context(habit, *, today=None, limit=7):
    today = today or date.today()
    return {
        "todays_entry": habit.entries.filter(date=today).first(),
        "recent_entries": get_recent_entries_for_habit(habit, limit=limit),
    }
