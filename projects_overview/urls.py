from django.urls import path

from .views import (
    project_create_view,
    project_detail_view,
    project_list_view,
    project_update_view,
)

app_name = "projects_overview"

urlpatterns = [
    path("", project_list_view, name="list"),
    path("create/", project_create_view, name="create"),
    path("<slug:slug>/", project_detail_view, name="detail"),
    path("<slug:slug>/edit/", project_update_view, name="edit"),
]
