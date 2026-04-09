from django.shortcuts import render

from .selectors import get_dashboard_context

def home(request):
    context = {}
    if request.user.is_authenticated:
        context = get_dashboard_context()
    return render(request, "dashboard/home.html", context)
