from django.urls import path

from .views import (
    habit_create_view,
    habit_detail_view,
    habit_list_view,
    habit_log_entry_view,
    habit_update_view,
)

app_name = "habits"

urlpatterns = [
    path("", habit_list_view, name="list"),
    path("create/", habit_create_view, name="create"),
    path("<slug:slug>/", habit_detail_view, name="detail"),
    path("<slug:slug>/edit/", habit_update_view, name="edit"),
    path("<slug:slug>/log/", habit_log_entry_view, name="log-entry"),
]
