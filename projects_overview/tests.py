from django.core.exceptions import ValidationError
from django.test import TestCase

from .services import create_project_snapshot, update_project_snapshot


class ProjectSnapshotServiceTests(TestCase):
    def test_create_project_generates_slug(self):
        project = create_project_snapshot(
            name="Dev Dashboard",
            description="",
            status="active",
            current_focus="Phase 6",
            next_step="Phase 7",
        )

        self.assertEqual(project.slug, "dev-dashboard")

    def test_update_project_changes_status_but_keeps_slug(self):
        project = create_project_snapshot(
            name="Dev Dashboard",
            description="",
            status="active",
            current_focus="Phase 6",
            next_step="Phase 7",
        )

        updated = update_project_snapshot(
            project=project,
            name="Dev Dashboard revised",
            description="Updated",
            status="paused",
            current_focus="Refine status",
            next_step="Resume later",
            is_active=False,
        )

        self.assertEqual(updated.slug, "dev-dashboard")
        self.assertEqual(updated.status, "paused")
        self.assertFalse(updated.is_active)


class ProjectSnapshotModelTests(TestCase):
    def test_slug_is_immutable(self):
        project = create_project_snapshot(
            name="Immutable project",
            description="",
            status="active",
            current_focus="",
            next_step="",
        )

        project.slug = "changed-slug"
        with self.assertRaises(ValidationError):
            project.full_clean()
