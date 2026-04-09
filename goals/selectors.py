from .models import Goal


def get_goals_for_list():
    return Goal.objects.all()


def get_active_goals():
    return Goal.objects.filter(status="active", is_archived=False)


def get_goal_by_slug(slug):
    return Goal.objects.filter(slug=slug)
