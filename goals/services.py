from django.db import transaction
from django.template.defaultfilters import slugify
from django.utils import timezone

from .models import Goal, GoalStatus


def _generate_unique_slug(title):
    base_slug = slugify(title) or "goal"
    slug = base_slug
    index = 2
    while Goal.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{index}"
        index += 1
    return slug


@transaction.atomic
def create_goal(*, title, description="", type, status, priority, deadline=None, is_archived=False):
    completed_at = timezone.now() if status == GoalStatus.COMPLETED else None
    goal = Goal(
        title=title,
        slug=_generate_unique_slug(title),
        description=description,
        type=type,
        status=status,
        priority=priority,
        deadline=deadline,
        completed_at=completed_at,
        is_archived=is_archived,
    )
    goal.full_clean()
    goal.save()
    return goal


@transaction.atomic
def update_goal(*, goal, title, description="", type, status, priority, deadline=None, is_archived=False):
    goal.title = title
    goal.description = description
    goal.type = type
    goal.status = status
    goal.priority = priority
    goal.deadline = deadline
    goal.is_archived = is_archived

    if status == GoalStatus.COMPLETED and goal.completed_at is None:
        goal.completed_at = timezone.now()
    elif status != GoalStatus.COMPLETED:
        goal.completed_at = None

    goal.full_clean()
    goal.save()
    return goal
