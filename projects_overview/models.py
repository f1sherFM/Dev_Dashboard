from django.core.exceptions import ValidationError
from django.db import models


class ProjectStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    PAUSED = "paused", "Paused"
    ON_HOLD = "on_hold", "On hold"
    DONE = "done", "Done"


class ProjectSnapshot(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.ACTIVE,
    )
    current_focus = models.TextField(blank=True)
    next_step = models.TextField(blank=True)
    repo_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    started_at = models.DateField(blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_active", "name"]

    def __str__(self):
        return self.name

    def clean(self):
        if not self._state.adding:
            original = ProjectSnapshot.objects.filter(pk=self.pk).values_list("slug", flat=True).first()
            if original and original != self.slug:
                raise ValidationError({"slug": "Slug cannot be changed after creation."})
