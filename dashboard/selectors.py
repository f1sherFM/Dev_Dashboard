from datetime import date

from django.db.models import Prefetch
from django.urls import reverse

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
    habits_needing_log = [habit for habit in today_habits if not habit.today_entries]
    urgent_goals = [goal for goal in top_active_goals if goal.deadline][:3]
    attention_items = []

    if habits_needing_log:
        attention_items.append(
            {
                "title": "Log today's habits",
                "description": f"{len(habits_needing_log)} habit(s) still need an entry.",
                "action_label": "Open habits",
                "action_url": reverse("habits:list"),
            }
        )

    if todays_review is None:
        attention_items.append(
            {
                "title": "Finish today's review",
                "description": "Capture wins, problems, lessons, and tomorrow's plan before the day ends.",
                "action_label": "Open review",
                "action_url": reverse("reviews:today"),
            }
        )

    if urgent_goals:
        attention_items.append(
            {
                "title": "Check goal deadlines",
                "description": f"{urgent_goals[0].title} is the nearest active goal with a deadline.",
                "action_label": "View goals",
                "action_url": reverse("goals:list"),
            }
        )

    if active_projects and not active_projects[0].next_step:
        attention_items.append(
            {
                "title": "Set the next step",
                "description": f"{active_projects[0].name} is active but missing a clear next step.",
                "action_label": "Open projects",
                "action_url": reverse("projects_overview:list"),
            }
        )

    return {
        "today": today,
        "today_habits": today_habits,
        "habits_needing_log": habits_needing_log,
        "today_habits_count": today_habits.count(),
        "completed_habits_count": sum(
            1 for habit in today_habits if habit.today_entries and habit.today_entries[0].value > 0
        ),
        "todays_review": todays_review,
        "top_active_goals": top_active_goals,
        "active_projects": active_projects,
        "attention_items": attention_items,
    }
