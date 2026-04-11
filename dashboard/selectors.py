from datetime import date
from datetime import timedelta

from django.db.models import Avg
from django.db.models import Prefetch
from django.urls import reverse
from django.utils import timezone

from goals.models import Goal
from habits.models import Habit, HabitEntry
from habits.selectors import get_habit_progress
from projects_overview.models import ProjectSnapshot
from reviews.models import DailyReview
from reviews.selectors import get_weekly_reflection


def get_week_range(reference_date=None):
    reference_date = reference_date or timezone.localdate()
    week_start = reference_date - timedelta(days=reference_date.weekday())
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


def _build_week_link(target_date):
    return f"{reverse('dashboard:weekly')}?date={target_date.isoformat()}"


def get_weekly_summary(reference_date=None):
    reference_date = reference_date or timezone.localdate()
    week_start, week_end = get_week_range(reference_date=reference_date)
    current_week_start, current_week_end = get_week_range(reference_date=timezone.localdate())
    weekly_reflection = get_weekly_reflection(reference_date=reference_date)

    habits = list(Habit.objects.filter(is_active=True).order_by("name"))
    for habit in habits:
        weekly_count = habit.entries.filter(date__range=(week_start, week_end), value__gt=0).count()
        habit.weekly_completion_count = weekly_count
        habit.last_completed_date = get_habit_progress(habit, today=week_end)["last_completed_date"]

    habits_with_no_completions = [habit for habit in habits if habit.weekly_completion_count == 0]
    habits_completed_multiple_times = [habit for habit in habits if habit.weekly_completion_count >= 2]
    total_weekly_habit_completions = sum(habit.weekly_completion_count for habit in habits)

    reviews_this_week = DailyReview.objects.filter(date__range=(week_start, week_end)).order_by("date")
    review_averages = reviews_this_week.aggregate(
        overall_score_avg=Avg("overall_score"),
        energy_level_avg=Avg("energy_level"),
        focus_score_avg=Avg("focus_score"),
    )

    active_goals = Goal.objects.filter(status="active", is_archived=False).order_by("deadline", "-created_at")
    goals_completed_this_week = Goal.objects.filter(completed_at__date__range=(week_start, week_end)).order_by(
        "-completed_at"
    )
    goals_near_deadline = active_goals.filter(deadline__range=(week_start, week_end))

    active_projects = ProjectSnapshot.objects.filter(is_active=True).order_by("name")
    stale_projects = active_projects.filter(last_updated__lt=week_start - timedelta(days=14))

    if week_start < current_week_start:
        week_label = "past week"
    elif week_start > current_week_start:
        week_label = "future week"
    else:
        week_label = "current week"

    return {
        "reference_date": reference_date,
        "week_start": week_start,
        "week_end": week_end,
        "current_week_start": current_week_start,
        "current_week_end": current_week_end,
        "is_current_week": week_start == current_week_start,
        "week_label": week_label,
        "previous_week_url": _build_week_link(week_start - timedelta(days=1)),
        "next_week_url": _build_week_link(week_end + timedelta(days=1)),
        "current_week_url": reverse("dashboard:weekly"),
        "habits": habits,
        "habits_with_no_completions": habits_with_no_completions,
        "habits_completed_multiple_times": habits_completed_multiple_times,
        "total_weekly_habit_completions": total_weekly_habit_completions,
        "review_count": reviews_this_week.count(),
        "review_dates": [review.date for review in reviews_this_week],
        "review_averages": review_averages,
        "weekly_reflection": weekly_reflection,
        "weekly_reflection_url": f"{reverse('reviews:weekly-reflection')}?date={week_start.isoformat()}",
        "active_goals": active_goals,
        "goals_completed_this_week": goals_completed_this_week,
        "goals_near_deadline": goals_near_deadline,
        "active_projects": active_projects,
        "stale_projects": stale_projects,
    }


def get_dashboard_context(*, today=None):
    today = today or timezone.localdate()

    today_habits = Habit.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "entries", queryset=HabitEntry.objects.filter(date=today),
            to_attr="today_entries",
        )
    )
    today_habits = list(today_habits)
    for habit in today_habits:
        habit.today_entries = [entry for entry in habit.today_entries if entry.date == today]
        habit.progress = get_habit_progress(habit, today=today)
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
        "today_habits_count": len(today_habits),
        "completed_habits_count": sum(
            1 for habit in today_habits if habit.today_entries and habit.today_entries[0].value > 0
        ),
        "todays_review": todays_review,
        "top_active_goals": top_active_goals,
        "active_projects": active_projects,
        "attention_items": attention_items,
    }
