from django.urls import path

from .views import review_detail_view, review_history_view, today_review_view

app_name = "reviews"

urlpatterns = [
    path("", today_review_view, name="today"),
    path("history/", review_history_view, name="history"),
    path("<slug:review_date>/", review_detail_view, name="detail"),
]
