from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client, TestCase

from .models import DailyReview, WeeklyReflection
from .selectors import get_weekly_reflection
from .services import (
    create_or_update_review,
    create_or_update_weekly_reflection,
    get_weekly_reflection_by_date,
)


class ReviewServiceTests(TestCase):
    def test_create_or_update_review_keeps_one_row_per_date(self):
        first = create_or_update_review(
            date=date(2026, 4, 9),
            mood="good",
            energy_level=7,
            focus_score=8,
            wins="Started well",
            problems="",
            lessons="Keep going",
            tomorrow_plan="Continue",
            overall_score=8,
        )
        second = create_or_update_review(
            date=date(2026, 4, 9),
            mood="great",
            energy_level=9,
            focus_score=9,
            wins="Updated",
            problems="Minor delay",
            lessons="Plan tighter",
            tomorrow_plan="Ship next phase",
            overall_score=9,
        )

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(DailyReview.objects.filter(date=date(2026, 4, 9)).count(), 1)
        self.assertEqual(second.mood, "great")
        self.assertEqual(second.overall_score, 9)

    def test_create_or_update_weekly_reflection_normalizes_to_monday_and_updates_existing_row(self):
        first = create_or_update_weekly_reflection(
            reference_date=date(2026, 4, 9),
            wins="Good shipping week",
            problems="Fatigue",
            lessons="Keep scope tight",
            next_week_focus="Finish release work",
        )
        second = create_or_update_weekly_reflection(
            reference_date=date(2026, 4, 11),
            wins="Updated wins",
            problems="Updated problems",
            lessons="Updated lessons",
            next_week_focus="Updated focus",
        )

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(second.week_start_date, date(2026, 4, 6))
        self.assertEqual(WeeklyReflection.objects.filter(week_start_date=date(2026, 4, 6)).count(), 1)
        self.assertEqual(second.next_week_focus, "Updated focus")

    def test_get_weekly_reflection_by_date_returns_same_week_record(self):
        reflection = create_or_update_weekly_reflection(
            reference_date=date(2026, 4, 8),
            wins="Wins",
            problems="Problems",
            lessons="Lessons",
            next_week_focus="Focus",
        )

        fetched = get_weekly_reflection_by_date(reference_date=date(2026, 4, 12))

        self.assertEqual(fetched.pk, reflection.pk)


class WeeklyReflectionSelectorTests(TestCase):
    def test_get_weekly_reflection_accepts_reference_date(self):
        reflection = WeeklyReflection.objects.create(
            week_start_date=date(2026, 4, 6),
            wins="Wins",
            problems="Problems",
            lessons="Lessons",
            next_week_focus="Focus",
        )

        fetched = get_weekly_reflection(reference_date=date(2026, 4, 10))

        self.assertEqual(fetched.pk, reflection.pk)


class ReviewModelTests(TestCase):
    def test_one_review_per_date_is_enforced(self):
        DailyReview.objects.create(
            date=date(2026, 4, 9),
            mood="good",
            energy_level=7,
            focus_score=8,
            wins="",
            problems="",
            lessons="",
            tomorrow_plan="",
            overall_score=8,
        )

        with self.assertRaises(IntegrityError):
            DailyReview.objects.create(
                date=date(2026, 4, 9),
                mood="great",
                energy_level=9,
                focus_score=9,
                wins="",
                problems="",
                lessons="",
                tomorrow_plan="",
                overall_score=9,
            )

    def test_one_weekly_reflection_per_week_is_enforced(self):
        WeeklyReflection.objects.create(
            week_start_date=date(2026, 4, 6),
            wins="Wins",
            problems="Problems",
            lessons="Lessons",
            next_week_focus="Focus",
        )

        with self.assertRaises(IntegrityError):
            WeeklyReflection.objects.create(
                week_start_date=date(2026, 4, 6),
                wins="More wins",
                problems="More problems",
                lessons="More lessons",
                next_week_focus="More focus",
            )


class ReviewHtmxFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewuser", password="pass12345")
        self.client = Client()
        self.client.login(username="reviewuser", password="pass12345")

    def test_htmx_save_review_returns_refreshed_block_and_saves_review(self):
        response = self.client.post(
            "/reviews/",
            {
                "date": "2026-04-09",
                "mood": "good",
                "energy_level": "7",
                "focus_score": "8",
                "wins": "Saved with HTMX",
                "problems": "",
                "lessons": "Stay simple",
                "tomorrow_plan": "Continue",
                "overall_score": "8",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Saved")
        self.assertEqual(DailyReview.objects.filter(date=date(2026, 4, 9)).count(), 1)


class WeeklyReflectionFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="weeklyreflectionuser", password="pass12345")
        self.client = Client()
        self.client.login(username="weeklyreflectionuser", password="pass12345")

    def test_weekly_reflection_page_creates_reflection_for_normalized_week(self):
        response = self.client.post(
            "/reviews/weekly-reflection/?date=2026-04-09",
            {
                "wins": "Strong week",
                "problems": "Low energy",
                "lessons": "Protect focus",
                "next_week_focus": "Ship carefully",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(WeeklyReflection.objects.filter(week_start_date=date(2026, 4, 6)).count(), 1)

    def test_weekly_reflection_page_edits_existing_reflection(self):
        WeeklyReflection.objects.create(
            week_start_date=date(2026, 4, 6),
            wins="Old wins",
            problems="Old problems",
            lessons="Old lessons",
            next_week_focus="Old focus",
        )

        response = self.client.post(
            "/reviews/weekly-reflection/?date=2026-04-10",
            {
                "wins": "New wins",
                "problems": "New problems",
                "lessons": "New lessons",
                "next_week_focus": "New focus",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(WeeklyReflection.objects.filter(week_start_date=date(2026, 4, 6)).count(), 1)
        self.assertEqual(WeeklyReflection.objects.get(week_start_date=date(2026, 4, 6)).wins, "New wins")
