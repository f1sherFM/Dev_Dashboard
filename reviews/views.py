from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .forms import DailyReviewForm
from .selectors import get_review_by_date, get_reviews_for_history
from .services import create_or_update_review


def _render_today_review_block(request, *, form, review, today):
    return render(
        request,
        "reviews/partials/_today_review_block.html",
        {"form": form, "review": review, "today": today},
    )


@login_required
def today_review_view(request):
    today = date.today()
    review = get_review_by_date(today).first()
    form = DailyReviewForm(request.POST or None, instance=review, initial={"date": today})
    if request.method == "POST" and form.is_valid():
        review = create_or_update_review(**form.cleaned_data)
        form = DailyReviewForm(instance=review)
        if request.headers.get("HX-Request") == "true":
            return _render_today_review_block(request, form=form, review=review, today=today)

    if request.headers.get("HX-Request") == "true":
        response = _render_today_review_block(request, form=form, review=review, today=today)
        if form.errors:
            response.status_code = 400
        return response

    return render(
        request,
        "reviews/today_review.html",
        {"form": form, "review": review, "today": today},
    )


@login_required
def review_history_view(request):
    return render(
        request,
        "reviews/review_history.html",
        {"reviews": get_reviews_for_history()},
    )


@login_required
def review_detail_view(request, review_date):
    review = get_object_or_404(get_review_by_date(review_date))
    return render(request, "reviews/review_detail.html", {"review": review})
