from datetime import date
from datetime import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

from dashboard.selectors import get_dashboard_context, get_week_range, get_weekly_summary
from goals.models import Goal
from habits.models import Habit, HabitEntry
from projects_overview.models import ProjectSnapshot
from reviews.models import DailyReview, WeeklyReflection


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

    def test_get_week_range_returns_monday_to_sunday(self):
        week_start, week_end = get_week_range(reference_date=date(2026, 4, 9))

        self.assertEqual(week_start, date(2026, 4, 6))
        self.assertEqual(week_end, date(2026, 4, 12))

    def test_get_weekly_summary_aggregates_cross_domain_data(self):
        reference_date = date(2026, 3, 12)
        habit_a = Habit.objects.create(
            name="Write",
            slug="write",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )
        habit_b = Habit.objects.create(
            name="Workout",
            slug="workout",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )
        HabitEntry.objects.create(habit=habit_a, date=date(2026, 3, 10), value=1, note="")
        HabitEntry.objects.create(habit=habit_a, date=date(2026, 3, 12), value=1, note="")
        HabitEntry.objects.create(habit=habit_b, date=date(2026, 3, 11), value=0, note="")

        Goal.objects.create(
            title="Active goal",
            slug="active-goal",
            description="",
            type="career",
            status="active",
            priority="high",
            deadline=date(2026, 3, 13),
            is_archived=False,
        )
        Goal.objects.create(
            title="Completed goal",
            slug="completed-goal",
            description="",
            type="career",
            status="completed",
            priority="medium",
            completed_at=timezone.make_aware(datetime(2026, 3, 11, 10, 0)),
            is_archived=False,
        )
        DailyReview.objects.create(
            date=date(2026, 3, 10),
            mood="good",
            energy_level=7,
            focus_score=8,
            wins="Good week",
            problems="",
            lessons="",
            tomorrow_plan="",
            overall_score=8,
        )
        DailyReview.objects.create(
            date=date(2026, 3, 12),
            mood="great",
            energy_level=9,
            focus_score=9,
            wins="Strong day",
            problems="",
            lessons="",
            tomorrow_plan="",
            overall_score=9,
        )
        ProjectSnapshot.objects.create(
            name="Active project",
            slug="active-project",
            description="",
            status="active",
            current_focus="Ship weekly summary",
            next_step="Polish page",
            last_updated=date(2026, 3, 12),
            is_active=True,
        )
        ProjectSnapshot.objects.create(
            name="Stale project",
            slug="stale-project",
            description="",
            status="paused",
            current_focus="Waiting",
            next_step="",
            last_updated=date(2026, 2, 20),
            is_active=True,
        )
        WeeklyReflection.objects.create(
            week_start_date=date(2026, 3, 9),
            wins="Kept momentum",
            problems="A few delays",
            lessons="Smaller scope wins",
            next_week_focus="Close open work",
        )

        summary = get_weekly_summary(reference_date=reference_date)

        self.assertEqual(summary["week_start"], date(2026, 3, 9))
        self.assertEqual(summary["week_end"], date(2026, 3, 15))
        self.assertEqual(summary["review_count"], 2)
        self.assertEqual(summary["review_dates"], [date(2026, 3, 10), date(2026, 3, 12)])
        self.assertEqual(summary["review_averages"]["overall_score_avg"], 8.5)
        habit_counts = {habit.slug: habit.weekly_completion_count for habit in summary["habits"]}
        self.assertEqual(habit_counts["write"], 2)
        self.assertEqual(habit_counts["workout"], 0)
        self.assertEqual(len(summary["habits_with_no_completions"]), 1)
        self.assertEqual(len(summary["habits_completed_multiple_times"]), 1)
        self.assertEqual(summary["goals_completed_this_week"].count(), 1)
        self.assertEqual(summary["goals_near_deadline"].count(), 1)
        self.assertEqual(summary["active_projects"].count(), 2)
        self.assertEqual(summary["stale_projects"].count(), 1)
        self.assertIsNotNone(summary["weekly_reflection"])
        self.assertEqual(summary["weekly_reflection"].week_start_date, date(2026, 3, 9))
        self.assertIn("date=2026-03-09", summary["weekly_reflection_url"])
        self.assertFalse(summary["is_current_week"])
        self.assertEqual(summary["week_label"], "past week")
        self.assertIn("date=2026-03-08", summary["previous_week_url"])
        self.assertIn("date=2026-03-16", summary["next_week_url"])


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


class DashboardWeeklyPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="weeklyuser", password="pass12345")
        Habit.objects.create(
            name="Write",
            slug="write",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )

    def test_weekly_page_renders_for_authenticated_user(self):
        client = Client()
        client.login(username="weeklyuser", password="pass12345")

        response = client.get("/dashboard/weekly/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weekly Summary")
        self.assertContains(response, "Habits")
        self.assertContains(response, "Reviews")
        self.assertContains(response, "Previous week")
        self.assertContains(response, "Next week")

    def test_weekly_page_accepts_date_query_parameter(self):
        client = Client()
        client.login(username="weeklyuser", password="pass12345")

        response = client.get("/dashboard/weekly/?date=2026-03-12")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "March 9, 2026")
        self.assertContains(response, "March 15, 2026")
        self.assertContains(response, "Back to current week")

    def test_weekly_page_shows_write_reflection_action_when_missing(self):
        client = Client()
        client.login(username="weeklyuser", password="pass12345")

        response = client.get("/dashboard/weekly/?date=2026-04-09")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weekly reflection")
        self.assertContains(response, "Write weekly reflection")

    def test_weekly_page_shows_existing_reflection_and_edit_action(self):
        WeeklyReflection.objects.create(
            week_start_date=date(2026, 4, 6),
            wins="Strong shipping",
            problems="Low energy",
            lessons="Stay focused",
            next_week_focus="Close the last gaps",
        )
        client = Client()
        client.login(username="weeklyuser", password="pass12345")

        response = client.get("/dashboard/weekly/?date=2026-04-09")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit weekly reflection")
        self.assertContains(response, "Strong shipping")
        self.assertContains(response, "Close the last gaps")
