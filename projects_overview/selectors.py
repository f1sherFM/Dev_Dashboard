from .models import ProjectSnapshot


def get_projects_for_list():
    return ProjectSnapshot.objects.all()


def get_active_projects():
    return ProjectSnapshot.objects.filter(is_active=True)


def get_project_by_slug(slug):
    return ProjectSnapshot.objects.filter(slug=slug)
