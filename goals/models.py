from django.core.exceptions import ValidationError
from django.db import models


class GoalType(models.TextChoices):
    PERSONAL = "personal", "Personal"
    CAREER = "career", "Career"
    HEALTH = "health", "Health"
    LEARNING = "learning", "Learning"


class GoalStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    PAUSED = "paused", "Paused"
    COMPLETED = "completed", "Completed"


class GoalPriority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


class Goal(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=GoalType.choices)
    status = models.CharField(
        max_length=20,
        choices=GoalStatus.choices,
        default=GoalStatus.ACTIVE,
    )
    priority = models.CharField(
        max_length=20,
        choices=GoalPriority.choices,
        default=GoalPriority.MEDIUM,
    )
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["is_archived", "deadline", "-created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        if not self._state.adding:
            original = Goal.objects.filter(pk=self.pk).values_list("slug", flat=True).first()
            if original and original != self.slug:
                raise ValidationError({"slug": "Slug cannot be changed after creation."})
