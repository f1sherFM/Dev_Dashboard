from datetime import date
from datetime import timedelta

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


def get_last_completed_date(habit):
    entry = habit.entries.filter(value__gt=0).order_by("-date").first()
    return entry.date if entry else None


def get_weekly_completion_count(habit, *, today=None):
    today = today or date.today()
    start = today - timedelta(days=6)
    return habit.entries.filter(date__range=(start, today), value__gt=0).count()


def get_current_streak(habit, *, today=None):
    today = today or date.today()
    completed_dates = set(
        habit.entries.filter(date__lte=today, value__gt=0).values_list("date", flat=True)
    )

    if today not in completed_dates:
        return 0

    streak = 0
    current_day = today
    while current_day in completed_dates:
        streak += 1
        current_day -= timedelta(days=1)
    return streak


def get_habit_progress(habit, *, today=None):
    today = today or date.today()
    return {
        "current_streak": get_current_streak(habit, today=today),
        "last_completed_date": get_last_completed_date(habit),
        "weekly_completion_count": get_weekly_completion_count(habit, today=today),
    }


def get_habit_detail_context(habit, *, today=None, limit=7):
    today = today or date.today()
    return {
        "todays_entry": habit.entries.filter(date=today).first(),
        "recent_entries": get_recent_entries_for_habit(habit, limit=limit),
        "progress": get_habit_progress(habit, today=today),
    }
