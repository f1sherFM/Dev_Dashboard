from datetime import date

from django.test import TestCase

from dashboard.selectors import get_dashboard_context
from goals.models import Goal
from habits.models import Habit, HabitEntry
from projects_overview.models import ProjectSnapshot
from reviews.models import DailyReview


class DashboardSelectorTests(TestCase):
    def test_dashboard_context_contains_expected_aggregated_blocks(self):
        today = date(2026, 4, 9)
        Goal.objects.create(
            title="Primary goal",
            slug="primary-goal",
            description="",
            type="career",
            status="active",
            priority="high",
            is_archived=False,
        )
        Habit.objects.create(
            name="Write",
            slug="write",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )
        habit = Habit.objects.get(slug="write")
        HabitEntry.objects.create(habit=habit, date=today, value=1, note="")
        ProjectSnapshot.objects.create(
            name="Dev Dashboard",
            slug="dev-dashboard",
            description="",
            status="active",
            current_focus="Homepage",
            next_step="HTMX",
            is_active=True,
        )
        DailyReview.objects.create(
            date=today,
            mood="good",
            energy_level=8,
            focus_score=8,
            wins="Built selector",
            problems="",
            lessons="Keep calm",
            tomorrow_plan="Continue",
            overall_score=8,
        )

        context = get_dashboard_context(today=today)

        self.assertEqual(context["today_habits_count"], 1)
        self.assertEqual(context["completed_habits_count"], 1)
        self.assertIsNotNone(context["todays_review"])
        self.assertEqual(context["top_active_goals"].count(), 1)
        self.assertEqual(context["active_projects"].count(), 1)
