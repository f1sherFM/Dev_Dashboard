from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


class MoodChoices(models.TextChoices):
    GREAT = "great", "Great"
    GOOD = "good", "Good"
    OKAY = "okay", "Okay"
    LOW = "low", "Low"
    BAD = "bad", "Bad"


class DailyReview(models.Model):
    date = models.DateField(unique=True)
    mood = models.CharField(max_length=20, choices=MoodChoices.choices)
    energy_level = models.PositiveSmallIntegerField()
    focus_score = models.PositiveSmallIntegerField()
    wins = models.TextField(blank=True)
    problems = models.TextField(blank=True)
    lessons = models.TextField(blank=True)
    tomorrow_plan = models.TextField(blank=True)
    overall_score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def clean(self):
        super().clean()
        for field_name in ("energy_level", "focus_score", "overall_score"):
            value = getattr(self, field_name)
            if value < 1 or value > 10:
                raise ValidationError({field_name: "Value must be between 1 and 10."})

    def __str__(self):
        return f"Review for {self.date}"


class WeeklyReflection(models.Model):
    week_start_date = models.DateField(unique=True)
    wins = models.TextField(blank=True)
    problems = models.TextField(blank=True)
    lessons = models.TextField(blank=True)
    next_week_focus = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-week_start_date"]

    def clean(self):
        super().clean()
        if self.week_start_date is None:
            return
        normalized_week_start = self.week_start_date - timedelta(days=self.week_start_date.weekday())
        if self.week_start_date != normalized_week_start:
            raise ValidationError({"week_start_date": "Week start date must be the Monday of that week."})

    def __str__(self):
        return f"Weekly reflection for {self.week_start_date}"
