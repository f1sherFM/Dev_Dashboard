from django.db import transaction
from django.template.defaultfilters import slugify

from .models import Habit, HabitEntry


def _generate_unique_slug(name):
    base_slug = slugify(name) or "habit"
    slug = base_slug
    index = 2
    while Habit.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{index}"
        index += 1
    return slug


@transaction.atomic
def create_habit(*, name, description="", frequency, target_count=1, unit="times", is_active=True):
    habit = Habit(
        name=name,
        slug=_generate_unique_slug(name),
        description=description,
        frequency=frequency,
        target_count=target_count,
        unit=unit,
        is_active=is_active,
    )
    habit.full_clean()
    habit.save()
    return habit


@transaction.atomic
def update_habit(*, habit, name, description="", frequency, target_count=1, unit="times", is_active=True):
    habit.name = name
    habit.description = description
    habit.frequency = frequency
    habit.target_count = target_count
    habit.unit = unit
    habit.is_active = is_active
    habit.full_clean()
    habit.save()
    return habit


@transaction.atomic
def log_habit_entry(*, habit, date, value, note=""):
    entry, created = HabitEntry.objects.get_or_create(
        habit=habit,
        date=date,
        defaults={"value": value, "note": note},
    )
    if not created:
        entry.value = value
        entry.note = note

    entry.full_clean()
    entry.save()
    return entry
