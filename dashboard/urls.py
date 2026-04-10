from django.urls import path

from .views import home, weekly_summary_view

app_name = "dashboard"

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/weekly/", weekly_summary_view, name="weekly"),
]
