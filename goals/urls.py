from django.urls import path

from .views import (
    goal_create_view,
    goal_detail_view,
    goal_list_view,
    goal_update_view,
)

app_name = "goals"

urlpatterns = [
    path("", goal_list_view, name="list"),
    path("create/", goal_create_view, name="create"),
    path("<slug:slug>/", goal_detail_view, name="detail"),
    path("<slug:slug>/edit/", goal_update_view, name="edit"),
]
