from django import forms

from .models import ProjectSnapshot


class ProjectSnapshotForm(forms.ModelForm):
    class Meta:
        model = ProjectSnapshot
        fields = (
            "name",
            "description",
            "status",
            "current_focus",
            "next_step",
            "repo_url",
            "demo_url",
            "started_at",
            "last_updated",
            "is_active",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "current_focus": forms.Textarea(attrs={"rows": 3}),
            "next_step": forms.Textarea(attrs={"rows": 3}),
            "started_at": forms.DateInput(attrs={"type": "date"}),
            "last_updated": forms.DateInput(attrs={"type": "date"}),
        }
