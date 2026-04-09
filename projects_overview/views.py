from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectSnapshotForm
from .selectors import get_project_by_slug, get_projects_for_list
from .services import create_project_snapshot, update_project_snapshot


@login_required
def project_list_view(request):
    return render(
        request,
        "projects_overview/project_list.html",
        {"projects": get_projects_for_list()},
    )


@login_required
def project_detail_view(request, slug):
    project = get_object_or_404(get_project_by_slug(slug))
    return render(request, "projects_overview/project_detail.html", {"project": project})


@login_required
def project_create_view(request):
    form = ProjectSnapshotForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = create_project_snapshot(**form.cleaned_data)
        return redirect("projects_overview:detail", slug=project.slug)

    return render(
        request,
        "projects_overview/project_form.html",
        {"form": form, "page_title": "Create Project"},
    )


@login_required
def project_update_view(request, slug):
    project = get_object_or_404(get_project_by_slug(slug))
    form = ProjectSnapshotForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        project = update_project_snapshot(project=project, **form.cleaned_data)
        return redirect("projects_overview:detail", slug=project.slug)

    return render(
        request,
        "projects_overview/project_form.html",
        {"form": form, "project": project, "page_title": "Edit Project"},
    )
