from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import HabitEntryForm, HabitForm
from .selectors import get_habit_by_slug, get_habits_for_list, get_habit_detail_context
from .services import create_habit, log_habit_entry, update_habit


def _render_habit_log_block(request, *, habit, form):
    context = {
        "habit": habit,
        "form": form,
        **get_habit_detail_context(habit, today=timezone.localdate()),
    }
    return render(request, "habits/partials/_habit_log_block.html", context)


@login_required
def habit_list_view(request):
    return render(
        request,
        "habits/habit_list.html",
        {"habits": get_habits_for_list()},
    )


@login_required
def habit_detail_view(request, slug):
    habit = get_object_or_404(get_habit_by_slug(slug))
    detail_context = get_habit_detail_context(habit, today=timezone.localdate())
    return render(
        request,
        "habits/habit_detail.html",
        {
            "habit": habit,
            "entry_form": HabitEntryForm(initial={"date": timezone.localdate()}),
            **detail_context,
        },
    )


@login_required
def habit_create_view(request):
    form = HabitForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        habit = create_habit(**form.cleaned_data)
        return redirect("habits:detail", slug=habit.slug)

    return render(request, "habits/habit_form.html", {"form": form, "page_title": "Create Habit"})


@login_required
def habit_update_view(request, slug):
    habit = get_object_or_404(get_habit_by_slug(slug))
    form = HabitForm(request.POST or None, instance=habit)
    if request.method == "POST" and form.is_valid():
        habit = update_habit(habit=habit, **form.cleaned_data)
        return redirect("habits:detail", slug=habit.slug)

    return render(
        request,
        "habits/habit_form.html",
        {"form": form, "habit": habit, "page_title": "Edit Habit"},
    )


@login_required
def habit_log_entry_view(request, slug):
    habit = get_object_or_404(get_habit_by_slug(slug))
    form = HabitEntryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        log_habit_entry(habit=habit, **form.cleaned_data)
        if request.headers.get("HX-Request") == "true":
            fresh_form = HabitEntryForm(initial={"date": timezone.localdate()})
            return _render_habit_log_block(request, habit=habit, form=fresh_form)
        return redirect("habits:detail", slug=habit.slug)

    if request.headers.get("HX-Request") == "true":
        response = _render_habit_log_block(request, habit=habit, form=form)
        if form.errors:
            response.status_code = 400
        return response

    return render(
        request,
        "habits/habit_entry_form.html",
        {"form": form, "habit": habit},
    )
