from django import forms

from .models import DailyReview


class DailyReviewForm(forms.ModelForm):
    class Meta:
        model = DailyReview
        fields = (
            "date",
            "mood",
            "energy_level",
            "focus_score",
            "wins",
            "problems",
            "lessons",
            "tomorrow_plan",
            "overall_score",
        )
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "wins": forms.Textarea(attrs={"rows": 3}),
            "problems": forms.Textarea(attrs={"rows": 3}),
            "lessons": forms.Textarea(attrs={"rows": 3}),
            "tomorrow_plan": forms.Textarea(attrs={"rows": 3}),
        }
