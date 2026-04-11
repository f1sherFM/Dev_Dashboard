from datetime import timedelta

from django.db import transaction

from .models import DailyReview, WeeklyReflection


def _normalize_week_start(reference_date):
    return reference_date - timedelta(days=reference_date.weekday())


@transaction.atomic
def create_or_update_review(
    *,
    date,
    mood,
    energy_level,
    focus_score,
    wins="",
    problems="",
    lessons="",
    tomorrow_plan="",
    overall_score,
):
    review = DailyReview.objects.filter(date=date).first()
    if review is None:
        review = DailyReview(date=date)
    review.mood = mood
    review.energy_level = energy_level
    review.focus_score = focus_score
    review.wins = wins
    review.problems = problems
    review.lessons = lessons
    review.tomorrow_plan = tomorrow_plan
    review.overall_score = overall_score
    review.full_clean()
    review.save()
    return review


@transaction.atomic
def create_or_update_weekly_reflection(*, reference_date, wins="", problems="", lessons="", next_week_focus=""):
    week_start_date = _normalize_week_start(reference_date)
    reflection = WeeklyReflection.objects.filter(week_start_date=week_start_date).first()
    if reflection is None:
        reflection = WeeklyReflection(week_start_date=week_start_date)

    reflection.wins = wins
    reflection.problems = problems
    reflection.lessons = lessons
    reflection.next_week_focus = next_week_focus
    reflection.full_clean()
    reflection.save()
    return reflection


def get_weekly_reflection_by_date(*, reference_date):
    return WeeklyReflection.objects.filter(
        week_start_date=_normalize_week_start(reference_date)
    ).first()
