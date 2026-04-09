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

    def __str__(self):
        return f"Review for {self.date}"

    def clean(self):
        for field_name in ("energy_level", "focus_score", "overall_score"):
            value = getattr(self, field_name)
            if value < 1 or value > 10:
                raise ValidationError({field_name: "Value must be between 1 and 10."})
