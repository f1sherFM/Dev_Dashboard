from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client, TestCase

from .models import DailyReview
from .services import create_or_update_review


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
