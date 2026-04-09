from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GoalForm
from .selectors import get_goal_by_slug, get_goals_for_list
from .services import create_goal, update_goal


@login_required
def goal_list_view(request):
    return render(
        request,
        "goals/goal_list.html",
        {"goals": get_goals_for_list()},
    )


@login_required
def goal_detail_view(request, slug):
    goal = get_object_or_404(get_goal_by_slug(slug))
    return render(request, "goals/goal_detail.html", {"goal": goal})


@login_required
def goal_create_view(request):
    form = GoalForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        goal = create_goal(**form.cleaned_data)
        return redirect("goals:detail", slug=goal.slug)

    return render(request, "goals/goal_form.html", {"form": form, "page_title": "Create Goal"})


@login_required
def goal_update_view(request, slug):
    goal = get_object_or_404(get_goal_by_slug(slug))
    form = GoalForm(request.POST or None, instance=goal)
    if request.method == "POST" and form.is_valid():
        goal = update_goal(goal=goal, **form.cleaned_data)
        return redirect("goals:detail", slug=goal.slug)

    return render(
        request,
        "goals/goal_form.html",
        {"form": form, "goal": goal, "page_title": "Edit Goal"},
    )
