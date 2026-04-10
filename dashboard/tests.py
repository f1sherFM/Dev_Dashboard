from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

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

    def test_dashboard_context_includes_attention_items_for_open_daily_work(self):
        today = date(2026, 4, 9)
        Goal.objects.create(
            title="Near deadline",
            slug="near-deadline",
            description="",
            type="career",
            status="active",
            priority="high",
            deadline=today,
            is_archived=False,
        )
        Habit.objects.create(
            name="Review notes",
            slug="review-notes",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )
        ProjectSnapshot.objects.create(
            name="Shipping work",
            slug="shipping-work",
            description="",
            status="active",
            current_focus="Release polish",
            next_step="",
            is_active=True,
        )

        context = get_dashboard_context(today=today)

        titles = [item["title"] for item in context["attention_items"]]
        self.assertIn("Log today's habits", titles)
        self.assertIn("Finish today's review", titles)
        self.assertIn("Check goal deadlines", titles)
        self.assertIn("Set the next step", titles)


class DashboardHtmxFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dashboarduser", password="pass12345")
        self.habit = Habit.objects.create(
            name="Inbox zero",
            slug="inbox-zero",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )
        self.client = Client()
        self.client.login(username="dashboarduser", password="pass12345")

    def test_dashboard_htmx_habit_log_refreshes_dashboard_widget(self):
        today = timezone.localdate()
        response = self.client.post(
            f"/habits/{self.habit.slug}/log/",
            {
                "date": today.isoformat(),
                "value": "1",
                "note": "",
                "source": "dashboard",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Today's habits")
        self.assertContains(response, "logged")
        self.assertEqual(HabitEntry.objects.filter(habit=self.habit, date=today).count(), 1)
