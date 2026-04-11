from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import DailyReviewForm, WeeklyReflectionForm
from .selectors import get_review_by_date, get_reviews_for_history, get_weekly_reflection
from .services import create_or_update_review, create_or_update_weekly_reflection


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


@login_required
def weekly_reflection_view(request):
    raw_date = request.GET.get("date")
    reference_date = timezone.localdate()
    if raw_date:
        try:
            reference_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            reference_date = timezone.localdate()

    reflection = get_weekly_reflection(reference_date=reference_date)

    if request.method == "POST":
        form = WeeklyReflectionForm(request.POST, instance=reflection)
        if form.is_valid():
            reflection = create_or_update_weekly_reflection(
                reference_date=reference_date,
                wins=form.cleaned_data["wins"],
                problems=form.cleaned_data["problems"],
                lessons=form.cleaned_data["lessons"],
                next_week_focus=form.cleaned_data["next_week_focus"],
            )
            return redirect(f"{reverse('dashboard:weekly')}?date={reflection.week_start_date.isoformat()}")
    else:
        form = WeeklyReflectionForm(instance=reflection)

    return render(
        request,
        "reviews/weekly_reflection_form.html",
        {
            "form": form,
            "reflection": reflection,
            "reference_date": reference_date,
        },
    )
