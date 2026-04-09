from django.db import transaction

from .models import DailyReview


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
