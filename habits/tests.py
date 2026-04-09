from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client, TestCase

from .models import Habit, HabitEntry
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
        response = self.client.post(
            f"/habits/{self.habit.slug}/log/",
            {"date": "2026-04-09", "value": "1", "note": "quick log"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logged today")
        self.assertEqual(HabitEntry.objects.filter(habit=self.habit, date=date(2026, 4, 9)).count(), 1)
