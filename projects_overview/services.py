from django.db import transaction
from django.template.defaultfilters import slugify

from .models import ProjectSnapshot


def _generate_unique_slug(name):
    base_slug = slugify(name) or "project"
    slug = base_slug
    index = 2
    while ProjectSnapshot.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{index}"
        index += 1
    return slug


@transaction.atomic
def create_project_snapshot(
    *,
    name,
    description="",
    status,
    current_focus="",
    next_step="",
    repo_url="",
    demo_url="",
    started_at=None,
    last_updated=None,
    is_active=True,
):
    project = ProjectSnapshot(
        name=name,
        slug=_generate_unique_slug(name),
        description=description,
        status=status,
        current_focus=current_focus,
        next_step=next_step,
        repo_url=repo_url,
        demo_url=demo_url,
        started_at=started_at,
        last_updated=last_updated,
        is_active=is_active,
    )
    project.full_clean()
    project.save()
    return project


@transaction.atomic
def update_project_snapshot(
    *,
    project,
    name,
    description="",
    status,
    current_focus="",
    next_step="",
    repo_url="",
    demo_url="",
    started_at=None,
    last_updated=None,
    is_active=True,
):
    project.name = name
    project.description = description
    project.status = status
    project.current_focus = current_focus
    project.next_step = next_step
    project.repo_url = repo_url
    project.demo_url = demo_url
    project.started_at = started_at
    project.last_updated = last_updated
    project.is_active = is_active
    project.full_clean()
    project.save()
    return project
