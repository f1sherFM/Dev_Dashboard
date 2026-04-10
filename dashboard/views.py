from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .selectors import get_dashboard_context, get_weekly_summary

def home(request):
    context = {}
    if request.user.is_authenticated:
        context = get_dashboard_context()
    return render(request, "dashboard/home.html", context)


@login_required
def weekly_summary_view(request):
    reference_date = None
    raw_date = request.GET.get("date")
    if raw_date:
        try:
            reference_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            reference_date = None

    context = get_weekly_summary(reference_date=reference_date)
    return render(request, "dashboard/weekly_summary.html", context)
