from django.core.exceptions import ValidationError
from django.db import models


class HabitFrequency(models.TextChoices):
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    FLEXIBLE = "flexible", "Flexible"


class Habit(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=20,
        choices=HabitFrequency.choices,
        default=HabitFrequency.DAILY,
    )
    target_count = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=50, default="times")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_active", "name"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.target_count < 1:
            raise ValidationError({"target_count": "Target count must be at least 1."})

        if not self._state.adding:
            original = Habit.objects.filter(pk=self.pk).values_list("slug", flat=True).first()
            if original and original != self.slug:
                raise ValidationError({"slug": "Slug cannot be changed after creation."})


class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="entries")
    date = models.DateField()
    value = models.IntegerField(default=0)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["habit", "date"], name="unique_habit_entry_per_day")
        ]

    def __str__(self):
        return f"{self.habit.name} on {self.date}"
