from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("goals/", include("goals.urls")),
    path("habits/", include("habits.urls")),
    path("reviews/", include("reviews.urls")),
    path("projects/", include("projects_overview.urls")),
]
