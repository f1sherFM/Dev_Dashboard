from datetime import timedelta

from .models import DailyReview, WeeklyReflection


def get_review_by_date(review_date):
    return DailyReview.objects.filter(date=review_date)


def get_reviews_for_history():
    return DailyReview.objects.all()


def _normalize_week_start(reference_date):
    return reference_date - timedelta(days=reference_date.weekday())


def get_weekly_reflection(*, week_start_date=None, reference_date=None):
    if week_start_date is None and reference_date is None:
        return None

    normalized_week_start = week_start_date or reference_date
    normalized_week_start = _normalize_week_start(normalized_week_start)
    return WeeklyReflection.objects.filter(week_start_date=normalized_week_start).first()
