from .models import DailyReview


def get_review_by_date(review_date):
    return DailyReview.objects.filter(date=review_date)


def get_reviews_for_history():
    return DailyReview.objects.all()
