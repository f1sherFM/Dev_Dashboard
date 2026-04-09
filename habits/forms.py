from django import forms
from django.utils import timezone

from .models import Habit, HabitEntry


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ("name", "description", "frequency", "target_count", "unit", "is_active")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class HabitEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = self.initial.get("date") or timezone.localdate()

    class Meta:
        model = HabitEntry
        fields = ("date", "value", "note")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }
