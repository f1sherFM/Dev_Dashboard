from django import forms

from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ("title", "description", "type", "status", "priority", "deadline", "is_archived")
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 5}),
        }
