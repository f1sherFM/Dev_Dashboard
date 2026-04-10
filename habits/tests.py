from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client, TestCase
from django.utils import timezone

from .models import Habit, HabitEntry
from .selectors import (
    get_current_streak,
    get_last_completed_date,
    get_weekly_completion_count,
)
from .services import create_habit, log_habit_entry, update_habit


class HabitServiceTests(TestCase):
    def test_create_habit_generates_slug(self):
        habit = create_habit(
            name="Workout",
            description="Morning session",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )

        self.assertEqual(habit.slug, "workout")

    def test_update_habit_changes_fields_but_not_slug(self):
        habit = create_habit(
            name="Workout",
            description="Morning session",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )

        updated = update_habit(
            habit=habit,
            name="Workout revised",
            description="Updated",
            frequency="weekly",
            target_count=3,
            unit="times",
            is_active=False,
        )

        self.assertEqual(updated.slug, "workout")
        self.assertEqual(updated.target_count, 3)
        self.assertFalse(updated.is_active)

    def test_relogging_updates_existing_entry_for_same_day(self):
        habit = create_habit(
            name="Read",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )

        first = log_habit_entry(habit=habit, date=date(2026, 4, 9), value=1, note="done")
        second = log_habit_entry(habit=habit, date=date(2026, 4, 9), value=0, note="updated")

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(HabitEntry.objects.filter(habit=habit, date=date(2026, 4, 9)).count(), 1)
        self.assertEqual(second.value, 0)
        self.assertEqual(second.note, "updated")


class HabitModelTests(TestCase):
    def test_one_entry_per_day_constraint_is_enforced(self):
        habit = Habit.objects.create(
            name="Meditate",
            slug="meditate",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )
        HabitEntry.objects.create(habit=habit, date=date(2026, 4, 9), value=1, note="")

        with self.assertRaises(IntegrityError):
            HabitEntry.objects.create(habit=habit, date=date(2026, 4, 9), value=0, note="")


class HabitProgressSelectorTests(TestCase):
    def setUp(self):
        self.habit = create_habit(
            name="Progress habit",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )

    def test_current_streak_counts_consecutive_days_ending_today(self):
        today = date(2026, 4, 10)
        log_habit_entry(habit=self.habit, date=date(2026, 4, 8), value=1, note="")
        log_habit_entry(habit=self.habit, date=date(2026, 4, 9), value=1, note="")
        log_habit_entry(habit=self.habit, date=today, value=1, note="")

        self.assertEqual(get_current_streak(self.habit, today=today), 3)

    def test_current_streak_is_zero_when_today_not_completed(self):
        today = date(2026, 4, 10)
        log_habit_entry(habit=self.habit, date=date(2026, 4, 8), value=1, note="")
        log_habit_entry(habit=self.habit, date=date(2026, 4, 9), value=1, note="")

        self.assertEqual(get_current_streak(self.habit, today=today), 0)

    def test_streak_breaks_on_missing_day(self):
        today = date(2026, 4, 10)
        log_habit_entry(habit=self.habit, date=date(2026, 4, 7), value=1, note="")
        log_habit_entry(habit=self.habit, date=date(2026, 4, 9), value=1, note="")
        log_habit_entry(habit=self.habit, date=today, value=1, note="")

        self.assertEqual(get_current_streak(self.habit, today=today), 2)

    def test_weekly_completion_count_counts_only_value_greater_than_zero(self):
        today = date(2026, 4, 10)
        log_habit_entry(habit=self.habit, date=date(2026, 4, 4), value=1, note="")
        log_habit_entry(habit=self.habit, date=date(2026, 4, 7), value=2, note="")
        log_habit_entry(habit=self.habit, date=date(2026, 4, 8), value=0, note="")
        log_habit_entry(habit=self.habit, date=today, value=1, note="")

        self.assertEqual(get_weekly_completion_count(self.habit, today=today), 3)

    def test_last_completed_date_returns_most_recent_completed_day(self):
        log_habit_entry(habit=self.habit, date=date(2026, 4, 8), value=1, note="")
        log_habit_entry(habit=self.habit, date=date(2026, 4, 9), value=0, note="")
        log_habit_entry(habit=self.habit, date=date(2026, 4, 10), value=2, note="")

        self.assertEqual(get_last_completed_date(self.habit), date(2026, 4, 10))

    def test_value_zero_does_not_count_as_completion(self):
        today = date(2026, 4, 10)
        log_habit_entry(habit=self.habit, date=today, value=0, note="")

        self.assertEqual(get_current_streak(self.habit, today=today), 0)
        self.assertEqual(get_weekly_completion_count(self.habit, today=today), 0)
        self.assertIsNone(get_last_completed_date(self.habit))


class HabitHtmxFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="habituser", password="pass12345")
        self.habit = create_habit(
            name="Water",
            description="",
            frequency="daily",
            target_count=1,
            unit="times",
            is_active=True,
        )
        self.client = Client()
        self.client.login(username="habituser", password="pass12345")

    def test_htmx_log_entry_returns_refreshed_block_and_saves_entry(self):
        today = timezone.localdate()
        response = self.client.post(
            f"/habits/{self.habit.slug}/log/",
            {"date": today.isoformat(), "value": "1", "note": "quick log"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logged today")
        self.assertEqual(HabitEntry.objects.filter(habit=self.habit, date=today).count(), 1)
