from datetime import date

from django.db.models import Prefetch

from goals.models import Goal
from habits.models import Habit, HabitEntry
from projects_overview.models import ProjectSnapshot
from reviews.models import DailyReview


def get_dashboard_context(*, today=None):
    today = today or date.today()

    today_habits = Habit.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "entries",
            queryset=HabitEntry.objects.filter(date=today),
            to_attr="today_entries",
        )
    )
    top_active_goals = Goal.objects.filter(
        status="active",
        is_archived=False,
    ).order_by("deadline", "-created_at")[:5]
    active_projects = ProjectSnapshot.objects.filter(is_active=True).order_by("name")[:5]
    todays_review = DailyReview.objects.filter(date=today).first()

    return {
        "today": today,
        "today_habits": today_habits,
        "today_habits_count": today_habits.count(),
        "completed_habits_count": sum(
            1 for habit in today_habits if habit.today_entries and habit.today_entries[0].value > 0
        ),
        "todays_review": todays_review,
        "top_active_goals": top_active_goals,
        "active_projects": active_projects,
    }
